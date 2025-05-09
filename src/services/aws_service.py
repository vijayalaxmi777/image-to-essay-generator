import boto3
import os
from botocore.exceptions import ClientError
from ..utils.logger import setup_logger
from ..utils.exceptions import S3Error, RekognitionError
from ..config import Config

logger = setup_logger(__name__)

class AWSService:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=Config.AWS_ACCESS_KEY,
            aws_secret_access_key=Config.AWS_SECRET_KEY,
            region_name=Config.AWS_REGION
        )
        
        self.rekognition_client = boto3.client(
            'rekognition',
            aws_access_key_id=Config.AWS_ACCESS_KEY,
            aws_secret_access_key=Config.AWS_SECRET_KEY,
            region_name=Config.AWS_REGION
        )

    def download_image(self, bucket: str, image_key: str, local_path: str) -> str:
        """Download image from S3 to local path"""
        try:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            self.s3_client.download_file(bucket, image_key, local_path)
            return local_path
        except ClientError as e:
            raise S3Error(f"Error downloading image: {str(e)}")

    def analyze_image(self, bucket: str, image_key: str) -> dict:
        try:
            response = self.rekognition_client.detect_labels(
                Image={
                    'S3Object': {
                        'Bucket': bucket,
                        'Name': image_key
                    }
                },
                MaxLabels=Config.MAX_LABELS,
                MinConfidence=Config.REKOGNITION_CONFIDENCE
            )

            scenes = []
            objects = []
            
            for label in response['Labels']:
                if label['Confidence'] > 90:
                    if any(parent['Name'] == 'Scene' for parent in label.get('Parents', [])):
                        scenes.append(label['Name'])
                    else:
                        objects.append(label['Name'])

            return {
                'scenes': scenes,
                'objects': objects
            }

        except ClientError as e:
            raise RekognitionError(f"Rekognition error: {str(e)}")

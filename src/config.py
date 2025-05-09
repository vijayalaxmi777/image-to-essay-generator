import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    S3_BUCKET = os.getenv('S3_BUCKET')
    
    # Model Configuration
    MODEL_NAME = os.getenv('MODEL_NAME', 'facebook/opt-2.7b')
    REKOGNITION_CONFIDENCE = 70
    MAX_LABELS = 20

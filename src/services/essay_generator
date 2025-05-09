import os
import tempfile
from .aws_service import AWSService
from .model_service import ModelService
from ..utils.logger import setup_logger
from ..utils.exceptions import ImageProcessingError

logger = setup_logger(__name__)

class EssayGenerator:
    def __init__(self):
        self.aws_service = AWSService()
        self.model_service = ModelService()

    def generate(self, bucket: str, image_key: str, use_blip: bool = False) -> dict:
        try:
            # Analyze image with Rekognition
            logger.info("Analyzing image with Rekognition...")
            image_analysis = self.aws_service.analyze_image(bucket, image_key)
            
            if use_blip:
                # Download image for BLIP processing
                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                    local_path = temp_file.name
                    self.aws_service.download_image(bucket, image_key, local_path)
                    
                    # Generate essay using BLIP
                    logger.info("Generating essay using BLIP...")
                    essay = self.model_service.generate_essay_with_blip(local_path)
                    
                    # Clean up
                    os.unlink(local_path)
            else:
                # Generate essay using Rekognition analysis
                logger.info("Generating essay...")
                essay = self.model_service.generate_essay(image_analysis)
            
            return {
                'analysis': image_analysis,
                'essay': essay
            }

        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            raise ImageProcessingError(str(e))

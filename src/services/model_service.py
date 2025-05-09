from transformers import pipeline
from ..utils.logger import setup_logger
from ..utils.exceptions import ModelError
from ..config import Config

logger = setup_logger(__name__)

class ModelService:
    def __init__(self):
        try:
            # Initialize the text generation pipeline
            self.generator = pipeline(
                'text-generation',
                model=Config.MODEL_NAME,
                device='cuda' if torch.cuda.is_available() else 'cpu'
            )
            logger.info(f"Model loaded successfully: {Config.MODEL_NAME}")
        except Exception as e:
            raise ModelError(f"Error loading model: {str(e)}")

    def generate_essay(self, image_analysis: dict) -> str:
        try:
            # Create prompt for the model
            prompt = f"""
            Write a descriptive essay about an image containing:
            Scenes: {', '.join(image_analysis['scenes'])}
            Objects: {', '.join(image_analysis['objects'])}
            Describe the scene, the relationships between objects, and the overall mood.
            """

            # Generate text
            response = self.generator(
                prompt,
                max_length=500,
                num_return_sequences=1,
                temperature=0.7,
                top_p=0.9
            )

            # Extract and clean the generated text
            generated_text = response[0]['generated_text']
            # Remove the prompt from the generated text
            essay = generated_text[len(prompt):].strip()
            
            return essay

        except Exception as e:
            raise ModelError(f"Text generation error: {str(e)}")

    def generate_essay_with_blip(self, image_path: str) -> str:
        """Alternative method using BLIP model for image captioning"""
        try:
            from transformers import BlipProcessor, BlipForConditionalGeneration
            import torch
            from PIL import Image

            processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

            # Load and process image
            image = Image.open(image_path)
            inputs = processor(image, return_tensors="pt")

            # Generate caption
            output = model.generate(**inputs, max_length=150)
            caption = processor.decode(output[0], skip_special_tokens=True)

            # Generate detailed description based on caption
            prompt = f"Based on the image caption: '{caption}', write a detailed descriptive essay."
            
            response = self.generator(
                prompt,
                max_length=500,
                num_return_sequences=1,
                temperature=0.7
            )

            return response[0]['generated_text']

        except Exception as e:
            raise ModelError(f"Image captioning error: {str(e)}")

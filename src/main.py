from services.essay_generator import EssayGenerator
from utils.logger import setup_logger
from config import Config
import argparse

logger = setup_logger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Generate essay from image')
    parser.add_argument('--image-key', required=True, help='S3 image key')
    parser.add_argument('--use-blip', action='store_true', help='Use BLIP model for image captioning')
    args = parser.parse_args()

    try:
        generator = EssayGenerator()
        
        result = generator.generate(
            bucket=Config.S3_BUCKET,
            image_key=args.image_key,
            use_blip=args.use_blip
        )

        print("\nImage Analysis:")
        print("Scenes:", result['analysis']['scenes'])
        print("Objects:", result['analysis']['objects'])
        print("\nGenerated Essay:")
        print(result['essay'])

    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    main()

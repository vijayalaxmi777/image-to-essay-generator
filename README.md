# Image Essay Generator

Generate descriptive essays from images using AWS Rekognition and Hugging Face transformers.

## Features
- Image analysis using AWS Rekognition
- Essay generation using Hugging Face transformers
- Optional BLIP model for image captioning
- S3 integration for image storage
- Detailed scene and object detection

## Setup
1. Clone the repository:
```bash git clone https://github.com/yourusername/image-essay-generator.git```

2. Install dependencies:
```pip install -r requirements.txt```

3. Configure environment variables:
```cp .env.example .env``` Edit .env with your credentials

## Usage
python src/main.py --image-key path/to/image.jpg
Or use BLIP model:
python src/main.py --image-key path/to/image.jpg --use-blip

## Models Used
- Facebook OPT-2.7B for text generation 
- Salesforce BLIP for image captioning (optional) 
- AWS Rekognition for image analysis 

## License
MIT License

## To use this code:
1. Create a new GitHub repository
2. Clone it locally
3. Copy these files into the repository
4. Install dependencies
5. Configure AWS credentials
6. Run the application

Remember to:
- Handle model loading efficiently
- Consider model size and memory requirements
- Implement proper error handling for model inference
- Add model caching if needed
- Consider adding a model download progress bar
- Implement proper cleanup for temporary files

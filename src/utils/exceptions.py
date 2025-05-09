class ImageProcessingError(Exception):
    """Base exception for image processing errors"""
    pass

class S3Error(ImageProcessingError):
    """Exception for S3-related errors"""
    pass

class RekognitionError(ImageProcessingError):
    """Exception for Rekognition-related errors"""
    pass

class ModelError(ImageProcessingError):
    """Exception for model-related errors"""
    pass

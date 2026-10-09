import os
from PIL import Image
from django.core.exceptions import ValidationError
from django.conf import settings

MAX_IMAGE_SIZE = getattr(settings, 'DATA_UPLOAD_MAX_MEMORY_SIZE', 10485760)
MAX_PIXELS = 8192 * 8192
ALLOWED_FORMATS = ['JPEG', 'PNG', 'WEBP']

def validate_image_file(file):
    if file.size > MAX_IMAGE_SIZE:
        raise ValidationError("Image file exceeds the maximum allowed size (10MB).")
        
    try:
        # Prevent PIL from loading large images for safety against decompression bombs
        Image.MAX_IMAGE_PIXELS = MAX_PIXELS
        
        with Image.open(file) as img:
            img.verify() # Verify file integrity
            
            if img.format not in ALLOWED_FORMATS:
                raise ValidationError(f"Unsupported image format: {img.format}. Supported formats are JPEG, PNG, WEBP.")
    except Exception as e:
        if isinstance(e, ValidationError):
            raise
        raise ValidationError(f"Invalid image file: {str(e)}")
        
    file.seek(0)
    return True

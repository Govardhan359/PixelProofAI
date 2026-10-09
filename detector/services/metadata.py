from PIL import Image, ExifTags

def extract_metadata(file_path):
    import os
    metadata = {
        'dimensions': None,
        'format': None,
        'mode': None,
        'file_size_bytes': os.path.getsize(file_path) if isinstance(file_path, str) else None,
        'exif': {}
    }
    
    # If the file passed is unexpected, try to get path
    if not isinstance(file_path, str) and hasattr(file_path, 'path'):
        file_path = file_path.path
        
    if isinstance(file_path, str):
        metadata['file_size_bytes'] = os.path.getsize(file_path)
            
    try:
        with Image.open(file_path) as img:
            metadata['dimensions'] = img.size
            metadata['format'] = img.format
            metadata['mode'] = img.mode
            
            exif_data = img.getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = ExifTags.TAGS.get(tag_id, tag_id)
                    # Convert bytes to string safely
                    if isinstance(value, bytes):
                        try:
                            value = value.decode('utf-8', errors='replace')
                        except:
                            value = str(value)
                    # Keep basic tags that are useful but not too much binary data
                    if tag not in ['MakerNote', 'UserComment']:
                        metadata['exif'][str(tag)] = str(value)
    except Exception:
        pass
    
    # reset pointer
    if hasattr(file_path, 'seek'):
        file_path.seek(0)
        
    return metadata

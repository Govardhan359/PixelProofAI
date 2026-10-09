import time
import torch
import warnings
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification

# Global cache for the model
_processor = None
_model = None
_device = None

MODEL_ID = "umm-maybe/AI-image-detector"

class InferenceException(Exception):
    pass

def _get_device():
    global _device
    if _device is None:
        _device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    return _device

def get_model_and_processor():
    global _processor, _model
    
    if _processor is None or _model is None:
        try:
            device = _get_device()
            _processor = AutoImageProcessor.from_pretrained(MODEL_ID)
            _model = AutoModelForImageClassification.from_pretrained(MODEL_ID).to(device)
            _model.eval()
        except Exception as e:
            raise InferenceException(f"Failed to load model weights. Ensure you have an internet connection for the first run or cached weights available. Error: {str(e)}")
            
    return _processor, _model

def classify_image(file_path):
    """
    Run inference on a given image file.
    Returns:
        dict containing:
            - predicted_class: str
            - raw_scores: dict
            - model_identifier: str
            - model_version: str
            - inference_duration: float
    """
    start_time = time.time()
    device = _get_device()
    
    try:
        processor, model = get_model_and_processor()
    except InferenceException:
        raise
        
    try:
        with Image.open(file_path) as img:
            image = img.convert("RGB")
        
        inputs = processor(images=image, return_tensors="pt").to(device)
        
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            
        predicted_class_idx = logits.argmax(-1).item()
        predicted_class = model.config.id2label[predicted_class_idx]
        
        # Optionally convert logits to probabilities using softmax
        scores = torch.nn.functional.softmax(logits, dim=-1).squeeze().tolist()
        if not isinstance(scores, list):
            scores = [scores]
            
        raw_scores = {model.config.id2label[i]: score for i, score in enumerate(scores)}
        
    except Exception as e:
        raise InferenceException(f"Failed to process image during inference: {str(e)}")
        
    duration = time.time() - start_time
    
    return {
        "predicted_class": predicted_class,
        "raw_scores": raw_scores,
        "model_identifier": MODEL_ID,
        "model_version": getattr(model.config, 'transformers_version', 'unknown'),
        "inference_duration": duration,
        "device": str(device)
    }

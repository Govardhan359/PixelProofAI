import os
import csv
import json
import torch
import argparse
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification
from metrics import compute_metrics

def main(manifest_path, output_path, model_id="umm-maybe/AI-image-detector"):
    print(f"Loading {model_id}...")
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    processor = AutoImageProcessor.from_pretrained(model_id)
    model = AutoModelForImageClassification.from_pretrained(model_id).to(device)
    model.eval()
    
    y_true = []
    y_pred = []
    y_scores = []
    
    errors = []
    
    base_dir = os.path.dirname(manifest_path)
    
    if not os.path.exists(manifest_path):
        print("Manifest not found.")
        return
        
    print("Evaluating...")
    with open(manifest_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            img_rel_path = row.get('image_path')
            label = row.get('label') # 'human' or 'artificial'
            
            if not img_rel_path or not label:
                continue
                
            img_path = os.path.join(base_dir, img_rel_path)
            
            if not os.path.exists(img_path):
                errors.append(f"Missing file: {img_path}")
                continue
                
            try:
                img = Image.open(img_path).convert("RGB")
                inputs = processor(images=img, return_tensors="pt").to(device)
                
                with torch.no_grad():
                    outputs = model(**inputs)
                    logits = outputs.logits
                    
                scores = torch.nn.functional.softmax(logits, dim=-1).squeeze()
                
                idx = logits.argmax(-1).item()
                pred_label = model.config.id2label[idx]
                
                # Assume class 0=artificial, 1=human based on verify_model output
                artificial_idx = 0
                for k, v in model.config.id2label.items():
                    if v == 'artificial':
                        artificial_idx = k
                        
                ai_score = float(scores[artificial_idx].item())
                
                is_ai_true = (label.lower() == 'artificial')
                is_ai_pred = (pred_label == 'artificial')
                
                y_true.append(is_ai_true)
                y_pred.append(is_ai_pred)
                y_scores.append(ai_score)
                
            except Exception as e:
                errors.append(f"Error processing {img_path}: {str(e)}")
                
    metrics = compute_metrics(y_true, y_pred, y_scores)
    
    result = {
        'model_id': model_id,
        'metrics': metrics,
        'errors': errors[:10] # limit exposed errors
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
        
    print(f"Evaluation complete. Results saved to {output_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Evaluate Image Detector on a dataset")
    parser.add_argument('--manifest', type=str, required=True, help="Path to CSV manifest with 'image_path' and 'label' columns.")
    parser.add_argument('--output', type=str, default='eval_results.json', help="Output JSON path")
    args = parser.parse_args()
    
    main(args.manifest, args.output)

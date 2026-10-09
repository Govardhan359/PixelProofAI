# PixelProof AI - Research Documentation

## Overview
This directory contains the pipeline for evaluating the AI-generation image detection model robustness.

## Model source and checkpoint identifier
* **Model ID:** `umm-maybe/AI-image-detector` (Swin Transformer Architecture)
* **Source:** Hugging Face Hub (https://huggingface.co/umm-maybe/AI-image-detector)
* **Intended Use:** Binary classification of images to differentiate between `human` and `artificial` origins.

## Evaluation Pipeline
The pipeline requires a dataset formatted with a `manifest.csv` containing two columns:
- `image_path`: Relative path to the image.
- `label`: Either `human` or `artificial`.

### Commands
Run the base evaluation:
```powershell
python research/evaluate.py --manifest path/to/dataset/manifest.csv --output eval_results.json
```

## Known Limitations
* The model evaluates spatial and statistical anomalies. Repeated JPEG compression, blurring, or resizing can affect confidence levels.
* Results are uncalibrated probabilities directly derived from logits via Softmax.

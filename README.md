# PixelProof AI

Every Pixel Has a Story.

PixelProof AI is a research-oriented web application designed to differentiate between genuine human-authored photographs and AI-generated images using PyTorch and Hugging Face Transformers.

## Features
- **Local Machine Learning Inference**: Uses the `umm-maybe/AI-image-detector` pretrained model (Swin Transformer architecture) locally without exposing images to external APIs.
- **Image Metadata Extraction**: Evaluates dimensions, EXIF data, and other contextual metadata (does not rely on missing metadata as proof of forgery).
- **Responsive Web Interface**: Built with Django, HTML5, and Tailwind CSS.
- **Reporting & Dashboarding**: Keeps local history of performed analyses including score breakdown and processing time. Option to download findings in JSON format.
- **Research Evaluation Pipeline**: Independent scripts available for evaluating benchmark dataset sets, producing confusion matrices, F1-scores, and performance metrics.

## Setup Instructions (Windows 11 PowerShell)

1. **Clone or set up the repository:**
   Ensure you are in the project folder `PixelProofAI`.

2. **Create a virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   npm install
   ```
   *(Note: The first run downloads torch and transformers checkpoints locally, requiring several gigabytes of space.)*

4. **Environment Variables:**
   Copy `.env.example` to `.env` and configure your local settings.

5. **Apply Database Migrations:**
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Build Frontend Assets (Tailwind CSS):**
   ```powershell
   npm run build:css
   ```

7. **Run the Server:**
   ```powershell
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000`

## Automated Tests
To run the automated tests using `pytest`:
```powershell
.\venv\Scripts\activate
pytest
```

## Research Evaluation
For evaluation, prepare a CSV `manifest.csv` containing columns `image_path` (relative to the CSV) and `label` (human or artificial).
```powershell
python research/evaluate.py --manifest data/manifest.csv --output data/results.json
```

## Security & Privacy Notice
All uploads and inference processes remain localized to the host instance. Uploaded files do not leave the host machine. However, the system caches the model from Hugging Face on the very first start.

## License
Provided for educational and research purposes only. Make sure to adhere to the model checkpoints' license agreements for real-world usage.

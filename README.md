<div align="center">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen.svg" alt="Project Status">
  <img src="https://img.shields.io/badge/Python-3.x-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Django-5.x-darkgreen.svg" alt="Django Version">
  <img src="https://img.shields.io/badge/PyTorch-AI-orange.svg" alt="PyTorch">
  <img src="https://img.shields.io/badge/Tailwind-CSS-38B2AC.svg" alt="Tailwind CSS">
  
  <h1>🛡️ PixelProof AI</h1>
  <p><b>Every Pixel Has a Story.</b></p>
  <p>A powerful, privacy-first web application designed to confidently differentiate between genuine human-authored photographs and AI-generated images utilizing state-of-the-art vision transformers.</p>
</div>

<hr>

## 🚀 Overview

As generative AI continues to evolve, distinguishing reality from artificial creation is more critical than ever. **PixelProof AI** leverages cutting-edge deep learning techniques to analyze images and provide a comprehensive authenticity report. Built with robustness, privacy, and user experience in mind, all inference is processed entirely locally, ensuring that sensitive data never leaves your environment.

## ✨ Key Features

- **🧠 Local Machine Learning Inference:** Utilizes the `umm-maybe/AI-image-detector` pretrained model (based on the Swin Transformer architecture) locally via PyTorch and Hugging Face Transformers. No external API dependencies.
- **📊 Comprehensive PDF Reporting:** Generates user-friendly, downloadable PDF reports (powered by ReportLab) detailing the analysis breakdown, confidence scores, and processing metrics.
- **🎨 Color-Coded Visual Feedback:** Intuitive, responsive web interface that provides immediate, color-coded visual feedback based on the AI's detection confidence percentages.
- **🔍 Advanced History & Filtering:** Robust history dashboard allowing users to track previous analyses, with advanced filtering options by status and prediction outcomes.
- **🔒 Privacy-First Architecture:** Complete offline processing capability. Uploaded media and analysis data remain strictly on the host machine.
- **⚙️ Resilient File Handling:** Engineered with robust file management systems to prevent locking issues and ensure high reliability during concurrent uploads and analysis.
- **📈 Research Evaluation Pipeline:** Includes standalone modules for evaluating benchmark datasets, generating confusion matrices, computing F1-scores, and assessing model performance.

## 🛠️ Tech Stack

### Deep Learning & AI
- **[PyTorch](https://pytorch.org/)** - Core deep learning framework for tensor computation.
- **[Hugging Face Transformers](https://huggingface.co/)** - For loading and running state-of-the-art vision transformers.
- **[scikit-learn](https://scikit-learn.org/)** - For machine learning evaluation metrics and dataset processing.

### Backend Development
- **[Python](https://www.python.org/)** - Primary programming language.
- **[Django](https://www.djangoproject.com/)** - High-level Python Web framework encouraging rapid development and clean design.
- **[SQLite](https://www.sqlite.org/)** - Lightweight, disk-based database for managing application state and history.
- **[ReportLab](https://pypi.org/project/reportlab/)** - For dynamic, robust PDF document generation.

### Frontend Development
- **[Tailwind CSS (v4)](https://tailwindcss.com/)** - Utility-first CSS framework for rapid UI development and styling.
- **HTML5 & Vanilla JavaScript** - For structuring the interface and handling dynamic UI interactions.

### Testing & QA
- **[pytest & pytest-django](https://pytest.org/)** - For comprehensive automated unit and integration testing.

## ⚙️ Installation & Setup (Windows / PowerShell)

Ensure you have Python 3.x and Node.js installed on your system.

**1. Clone the repository and navigate into the project directory:**
```powershell
# Set your working directory to the project folder
cd PixelProofAI
```

**2. Initialize and activate a virtual environment:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**3. Install Python dependencies:**
*(Note: Initial setup requires downloading PyTorch and Hugging Face model checkpoints, which may take some time depending on your connection.)*
```powershell
pip install -r requirements.txt
```

**4. Install Node dependencies (For Tailwind CSS):**
```powershell
npm install
```

**5. Configure Environment Variables:**
Copy the template `.env` file and adjust any necessary configurations.
```powershell
cp .env.example .env
```

**6. Apply database migrations:**
```powershell
python manage.py makemigrations
python manage.py migrate
```

**7. Build Frontend CSS Assets:**
```powershell
npm run build:css
```

**8. Run the Development Server:**
```powershell
python manage.py runserver
```

> **Note:** Access the application locally at `http://127.0.0.1:8000`. On the very first run, the system will cache the Hugging Face model checkpoints, which may cause a slight initial delay.

## 🧪 Testing

To run the automated robust test suite via `pytest`:
```powershell
.\venv\Scripts\activate
pytest
```

## 📊 Research & Evaluation Pipeline

For dataset evaluation (e.g., benchmarking performance on a holdout set), prepare a `manifest.csv` containing two columns:
- `image_path` (relative to the CSV)
- `label` (human or artificial)

Run the standalone evaluation script:
```powershell
python research/evaluate.py --manifest data/manifest.csv --output data/results.json
```

## 🛡️ Security & Privacy Notice

PixelProof AI is built with privacy at its core. All file uploads, processing, and inferences are completely isolated to the host instance. No media is transmitted to external servers for validation. 

## 📜 License

Created for educational, portfolio, and research purposes. Please ensure compliance with the original `umm-maybe/AI-image-detector` model checkpoints' license agreements for any real-world edge deployment.

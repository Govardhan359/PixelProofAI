import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
import json
from .models import AnalysisRecord
from .services.inference import classify_image

@pytest.mark.django_db
def test_landing_page(client):
    response = client.get(reverse('detector:landing'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_dashboard_page(client):
    response = client.get(reverse('detector:dashboard'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_upload_invalid_format(client):
    # Try uploading a txt file masked as image
    txt_file = SimpleUploadedFile("test.txt", b"file_content", content_type="text/plain")
    response = client.post(reverse('detector:upload'), {'image': txt_file})
    assert response.status_code == 200
    assert 'error' in response.content.decode().lower() or 'supported formats' in response.content.decode()

@pytest.mark.django_db
def test_upload_valid_format(client, monkeypatch):
    # Mock inference to avoid loading huge weights in normal tests
    def mock_classify(path):
        return {
            'predicted_class': 'artificial',
            'raw_scores': {'artificial': 0.9, 'human': 0.1},
            'model_identifier': 'mock-model',
            'model_version': '1.0',
            'inference_duration': 0.5,
            'device': 'cpu'
        }
    monkeypatch.setattr('detector.views.classify_image', mock_classify)
    
    # Create valid image
    img = Image.new('RGB', (100, 100), color='red')
    img_io = BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    
    upload_file = SimpleUploadedFile("test.jpg", img_io.read(), content_type="image/jpeg")
    
    response = client.post(reverse('detector:upload'), {'image': upload_file})
    # Should redirect to result page
    assert response.status_code == 302
    
    # Check DB record
    record = AnalysisRecord.objects.first()
    assert record is not None
    assert record.status == 'COMPLETED'
    assert record.predicted_class == 'artificial'

@pytest.mark.django_db
def test_history_page(client):
    response = client.get(reverse('detector:history'))
    assert response.status_code == 200

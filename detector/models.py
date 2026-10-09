import uuid
from django.db import models
from django.contrib.auth.models import User

class AnalysisRecord(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, help_text="Optional associate user")
    original_filename = models.CharField(max_length=255)
    image = models.ImageField(upload_to='analyses/%Y/%m/')
    
    # Prediction details
    predicted_class = models.CharField(max_length=50, null=True, blank=True)
    raw_scores = models.JSONField(null=True, blank=True, help_text="Raw logits or probabilities")
    
    # Model details
    model_identifier = models.CharField(max_length=255, null=True, blank=True)
    model_version = models.CharField(max_length=50, null=True, blank=True)
    
    # Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    inference_duration = models.FloatField(null=True, blank=True, help_text="Inference time in seconds")
    image_metadata = models.JSONField(null=True, blank=True, help_text="EXIF and format details")
    error_category = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.original_filename} - {self.status}"
        
    @property
    def ai_percentage(self):
        if self.raw_scores and 'artificial' in self.raw_scores:
            return round(self.raw_scores['artificial'] * 100, 1)
        return 0

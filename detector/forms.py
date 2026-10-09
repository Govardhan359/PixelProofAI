from django import forms
from .models import AnalysisRecord
from .services.image_validation import validate_image_file

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = AnalysisRecord
        fields = ['image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            validate_image_file(image)
        return image

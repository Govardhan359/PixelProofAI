from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, DetailView, ListView, View
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Count

from .models import AnalysisRecord
from .forms import ImageUploadForm
from .services.metadata import extract_metadata
from .services.inference import classify_image, InferenceException
from .services.report_service import generate_report_pdf
import json

class LandingPageView(TemplateView):
    template_name = 'detector/landing.html'

class DashboardView(TemplateView):
    template_name = 'detector/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        records = AnalysisRecord.objects.all()
        
        context['total_analyses'] = records.count()
        context['human_count'] = records.filter(predicted_class='human').count()
        context['ai_count'] = records.filter(predicted_class='artificial').count()
        context['failed_count'] = records.filter(status='FAILED').count()
        context['recent_analyses'] = records.order_by('-created_at')[:5]
        return context

class ImageUploadView(CreateView):
    model = AnalysisRecord
    form_class = ImageUploadForm
    template_name = 'detector/upload.html'
    
    def form_valid(self, form):
        # Create record
        record = form.save(commit=False)
        record.original_filename = self.request.FILES['image'].name
        record.status = 'PROCESSING'
        record.save()
        record.image.close()
        
        try:
            # Extract metadata
            img_path = record.image.path
            md = extract_metadata(img_path)
            record.image_metadata = md
            
            # Predict
            res = classify_image(img_path)
            record.predicted_class = res['predicted_class']
            record.raw_scores = res['raw_scores']
            record.model_identifier = res['model_identifier']
            record.model_version = res['model_version']
            record.inference_duration = res['inference_duration']
            record.status = 'COMPLETED'
        except InferenceException as e:
            record.status = 'FAILED'
            record.error_category = str(e)
        except Exception as e:
            record.status = 'FAILED'
            record.error_category = f"System Error: {str(e)}"
            
        record.save()
        
        if record.status == 'FAILED':
            messages.error(self.request, f"Analysis failed: {record.error_category}")
            
        return redirect(reverse('detector:result', kwargs={'pk': record.pk}))

class AnalysisResultView(DetailView):
    model = AnalysisRecord
    template_name = 'detector/result.html'
    context_object_name = 'analysis'

class AnalysisHistoryView(ListView):
    model = AnalysisRecord
    template_name = 'detector/history.html'
    context_object_name = 'analyses'
    paginate_by = 10
    
    def get_queryset(self):
        qs = super().get_queryset()
        status_filter = self.request.GET.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
            
        prediction_filter = self.request.GET.get('prediction')
        if prediction_filter:
            qs = qs.filter(predicted_class=prediction_filter)
            
        return qs.order_by('-created_at')
        
class AnalysisDeleteView(View):
    def post(self, request, pk):
        record = get_object_or_404(AnalysisRecord, pk=pk)
        if record.image:
            try:
                record.image.delete(save=False)
            except OSError:
                # File might be locked by another process on Windows temporarily
                pass
        record.delete()
        messages.success(request, "Analysis deleted successfully.")
        return redirect('detector:history')

class ReportDownloadView(View):
    def get(self, request, pk):
        record = get_object_or_404(AnalysisRecord, pk=pk)
        pdf_bytes = generate_report_pdf(record)
        
        response = HttpResponse(
            pdf_bytes,
            content_type="application/pdf"
        )
        response['Content-Disposition'] = f'attachment; filename="report_{record.id}.pdf"'
        return response

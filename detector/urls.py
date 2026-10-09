from django.urls import path
from . import views

app_name = 'detector'

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('upload/', views.ImageUploadView.as_view(), name='upload'),
    path('result/<uuid:pk>/', views.AnalysisResultView.as_view(), name='result'),
    path('history/', views.AnalysisHistoryView.as_view(), name='history'),
    path('delete/<uuid:pk>/', views.AnalysisDeleteView.as_view(), name='delete'),
    path('report/<uuid:pk>/', views.ReportDownloadView.as_view(), name='report'),
]

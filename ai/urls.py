from django.urls import path
from .views import PDFUploadView,PDFQueryView


urlpatterns = [
    path('upload', PDFUploadView.as_view(), name='pdf-upload'),
    path('query/<int:document_id>', PDFQueryView.as_view(), name='pdf-query'),
    
]
from image_processing.views import image_metrics_view
from django.urls import path

urlpatterns = [
    path('driveU/', image_metrics_view)
]

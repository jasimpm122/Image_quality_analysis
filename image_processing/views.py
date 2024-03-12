from django.shortcuts import render
from image_processing.process_images import process_images
from image_processing.images import image_urls


def image_metrics_view(request):
    metrics = process_images(image_urls)
    print(metrics)
    return render(request, 'image_metrics.html', {'metrics': metrics})
        
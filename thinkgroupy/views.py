from django.shortcuts import render
from django.views.defaults import page_not_found


def index(request):
    return render(request, 'index.html')


def handler404(request, exception):
    return page_not_found(request, exception, 'error/error-404.html')


def handler500(request):
    return render(request, 'error/error-500.html')

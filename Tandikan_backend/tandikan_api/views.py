from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse

def index(request):
    return JsonResponse({"status": "API is running"})

def test(request):
    return JsonResponse({"message": "Hello from Django"})


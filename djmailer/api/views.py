from django.shortcuts import render
from django.http.response import JsonResponse

# Create your views here.
def hello_world(request):
    return JsonResponse({"msg":"hello django"})

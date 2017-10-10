# from django.shortcuts import render
# from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.decorators import api_view

# Create your views here.

# Simple view.
# def hello_world_simple(request):
#     return JsonResponse({"msg":"hello django"})


# APIView Class example.
class HelloWorldView(APIView):
    def get(self, request):
        return Response({"msg":"Hello Django from APIView"})

    def post(self, request):
        name = request.data.get("name")
        if not name:
            return Response({"error":"No name passed"})
        return Response({"msg":"Hello {}!".format(name)})


# APIView function example.
# @api_view(["GET","POST"])
# def hello_world_dec(request):
#     if request.method == "GET":
#         return Response({"msg":"Hello django from the get method"})
#
#     else:
#         name = request.data.get("name")
#         if not name:
#             return Response({"error":"No name passed"})
#         return Response({"msg":"Hello {}!".format(name)})

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import HelloWorldSerializer


# APIView Class example.
class HelloWorldView(APIView):
    def get(self, request):
        return Response({"msg":"Hello Django from APIView"})

    # def post(self, request):
    #     name = request.data.get("name")
    #     if not name:
    #         return Response({"error":"No name passed"})
    #     return Response({"msg":"Hello {}!".format(name)})

    def post(self, request):
        serializer = HelloWorldSerializer(data=request.data)
        if serializer.is_valid():
            valid_data = serializer.data

            name = valid_data.get("name")
            age = valid_data.get("age")

            return Response({"msg":"Hello {}, you're {} years old.".format(name, age)})
        else:
            return Response({"errors": serializer.errors})

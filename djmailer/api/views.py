from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import SubscriberSerializer
from .models import Subscriber


# APIView based class example.
"""
class SubscriberView(APIView):
    def get(self, request):
        all_subscribers = Subscriber.objects.all()
        serialized_subscribers = SubscriberSerializer(all_subscribers, many=True)
        return Response(serialized_subscribers.data)

    def post(self, request):
        serializer = SubscriberSerializer(data=request.data)
        if serializer.is_valid():
            subscriber_instance = Subscriber.objects.create(**serializer.data)
            return Response({"msg":"Created Subscriber {}".format(subscriber_instance.id)})
        else:
            return Response({"errors": serializer.errors})
"""


# Generic Views example.
"""
class SubscriberView(ListAPIView, CreateAPIView):
    serializer_class = SubscriberSerializer
    queryset = Subscriber.objects.all()
"""


# Using ListCreateAPIView example.
"""
class SubscriberView(ListCreateAPIView):
    serializer_class = SubscriberSerializer
    queryset = Subscriber.objects.all()
"""


# Using ModelViewSets.
class SubscriberViewSet(ModelViewSet):
    serializer_class = SubscriberSerializer
    queryset = Subscriber.objects.all()
    permission_classes = (IsAuthenticated,)

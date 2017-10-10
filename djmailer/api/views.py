from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SubscriberSerializer
from .models import Subscriber


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

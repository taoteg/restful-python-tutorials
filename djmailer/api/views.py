from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SubscriberSerializer
from .models import Subscriber


class SubscriberView(APIView):
    def get(self, request):
        # return Response({"msg":"Hello Django from SubscriberView"})
        all_subscribers = Subscriber.objects.all()
        serialized_subscribers = SubscriberSerializer(all_subscribers, many=True)
        return Response(serialized_subscribers.data)

    def post(self, request):
        serializer = SubscriberSerializer(data=request.data)
        if serializer.is_valid():
            # valid_data = serializer.data
            # name = valid_data.get("name")
            # age = valid_data.get("age")
            # return Response({"msg":"Hello {}, you're {} years old.".format(name, age)})
            subscriber_instance = Subscriber.objects.create(**serializer.data)
            return Response({"msg":"Created Subscriber {}".format(subscriber_instance.id)})
        else:
            return Response({"errors": serializer.errors})

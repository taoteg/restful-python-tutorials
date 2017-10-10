from rest_framework import serializers


class SubscriberSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    email = serializers.EmailField()

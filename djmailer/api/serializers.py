from rest_framework import serializers


class HelloWorldSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=6)
    age = serializers.IntegerField(required=False, min_value=9, default=10)

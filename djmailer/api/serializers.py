from rest_framework import serializers

from .models import Subscriber

# Serializer Example.
"""
class SubscriberSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    email = serializers.EmailField()
"""

# ModelSerializer Example.
class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = "__all__"      # use all fields in the model.

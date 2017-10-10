from django.conf.urls import url
from .views import HelloWorldView #, hello_world_simple, hello_world_dec

urlpatterns = [
    # url(r'^hello-simple', hello_world_simple, name="hello_world_simple"),
    url(r'^hello-world', HelloWorldView.as_view(), name="hello_world"),
    # url(r'^hello-dec', hello_world_dec, name="hello_world_dec"),
]

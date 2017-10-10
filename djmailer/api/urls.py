from django.conf.urls import url
from .views import SubscriberView

urlpatterns = [
    url(r'^subscriber', SubscriberView.as_view(), name="subscriber"),
]

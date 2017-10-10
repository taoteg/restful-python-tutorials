from django.conf.urls import url
from rest_framework.routers import SimpleRouter

# from .views import SubscriberView
from .views import SubscriberViewSet


"""
urlpatterns = [
    # ListCreateAPIView ruls.
    url(r'^subscriber', SubscriberView.as_view(), name="subscriber"),
]
"""


# ModelViewSet urls using Router.
router = SimpleRouter()
router.register("subscribers", SubscriberViewSet)


urlpatterns = router.urls

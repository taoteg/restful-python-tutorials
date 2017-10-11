from django.conf.urls import url

from rest_framework.routers import SimpleRouter
from rest_framework_jwt.views import obtain_jwt_token

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


# urlpatterns = router.urls
urlpatterns = router.urls + [
    url(r'^jwt-auth/', obtain_jwt_token),
]

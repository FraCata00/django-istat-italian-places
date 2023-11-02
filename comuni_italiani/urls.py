from django.urls import include
from rest_framework.urls import path
from rest_framework.routers import DefaultRouter

from comuni_italiani.views import (
    RegioniAPIView,
    ProvinciaAPIView,
    ComuneAPIView,
)

router = DefaultRouter()

router.register(r"regioni", RegioniAPIView, basename="regioni")
router.register(r"province", ProvinciaAPIView, basename="province")
router.register(r"comuni", ComuneAPIView, basename="comuni")


urlpatterns = [
    path("", include(router.urls)),
]

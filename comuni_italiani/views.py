from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView
from comuni_italiani.serializers import (
    RegioneSerializer,
    ProvinciaSerializer,
    ProvinciaRetrieveSerializer,
    ComuneSerializer,
)
from rest_framework import viewsets
from comuni_italiani.models import Regione, Provincia, Comune


class RegioniAPIView(viewsets.GenericViewSet, ListAPIView, RetrieveAPIView):
    # TIPS:
    # - use select_related() for ForeignKey and OneToOneField
    # - use prefetch_related() for ManyToManyField and reverse ForeignKey

    serializer_class = RegioneSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Regione.objects.all()
    search_fields = [
        "denomination",
        "geographic_partition",
        "code",
    ]


class ProvinciaAPIView(viewsets.GenericViewSet, ListAPIView, RetrieveAPIView):
    # TIPS:
    # - use select_related() for ForeignKey and OneToOneField
    # - use prefetch_related() for ManyToManyField and reverse ForeignKey

    permission_classes = [permissions.IsAuthenticated]
    queryset = (
        Provincia.objects.select_related("region").prefetch_related("cities").all()
    )
    search_fields = [
        "denomination",
        "geographic_partition",
        "code",
        "auto_code",
        "region__denomination",
        "region__code",
    ]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProvinciaRetrieveSerializer
        return ProvinciaSerializer


class ComuneAPIView(viewsets.GenericViewSet, ListAPIView, RetrieveAPIView):
    # TIPS:
    # - use select_related() for ForeignKey and OneToOneField
    # - use prefetch_related() for ManyToManyField and reverse ForeignKey

    serializer_class = ComuneSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comune.objects.select_related("province").all()
    search_fields = [
        "denomination",
        "geographic_partition",
        "code",
        "progressive",
        "province__denomination",
        "province__code",
    ]

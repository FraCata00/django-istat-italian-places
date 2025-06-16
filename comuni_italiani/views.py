from rest_framework import permissions, viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView

from comuni_italiani.filters import ComuneFilters, ProvinciaFilters, RegioneFilters
from comuni_italiani.models import Comune, Provincia, Regione
from comuni_italiani.serializers import (
    ComuneSerializer,
    ProvinciaRetrieveSerializer,
    ProvinciaSerializer,
    RegioneSerializer,
)


class RegioniAPIView(viewsets.GenericViewSet, ListAPIView, RetrieveAPIView):
    # TIPS:
    # - use select_related() for ForeignKey and OneToOneField
    # - use prefetch_related() for ManyToManyField and reverse ForeignKey

    serializer_class = RegioneSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Regione.objects.all()
    search_fields = [
        "^denomination",
        "geographic_partition",
        "code",
    ]
    filterset_class = RegioneFilters


class ProvinciaAPIView(viewsets.GenericViewSet, ListAPIView, RetrieveAPIView):
    # TIPS:
    # - use select_related() for ForeignKey and OneToOneField
    # - use prefetch_related() for ManyToManyField and reverse ForeignKey

    permission_classes = [permissions.IsAuthenticated]
    queryset = (
        Provincia.objects.select_related("region").prefetch_related("cities").all()
    )
    search_fields = [
        "^denomination",
        "geographic_partition",
        "code",
        "auto_code",
        "^region__denomination",
        "region__code",
    ]
    filterset_class = ProvinciaFilters

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
        "^denomination",
        "geographic_partition",
        "code",
        "progressive",
    ]
    filterset_class = ComuneFilters

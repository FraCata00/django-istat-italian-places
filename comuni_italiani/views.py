from django.db.models.functions import Length
from rest_framework.viewsets import ReadOnlyModelViewSet

from comuni_italiani.filters import ComuneFilters, ProvinciaFilters, RegioneFilters
from comuni_italiani.models import Comune, Provincia, Regione
from comuni_italiani.serializers import (
    ComuneSerializer,
    ProvinciaRetrieveSerializer,
    ProvinciaSerializer,
    RegioneSerializer,
)


class LengthOfDenominationROMV(ReadOnlyModelViewSet):
    """
    Mixin to order the queryset by the length of the denomination field.
    - only during the search
    """

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.query_params.get("search"):
            return queryset.order_by(Length("denomination"))
        # if not searching, return the default queryset
        return queryset


class RegioniAPIView(LengthOfDenominationROMV):
    # TIPS:
    # - use select_related() for ForeignKey and OneToOneField
    # - use prefetch_related() for ManyToManyField and reverse ForeignKey

    serializer_class = RegioneSerializer
    queryset = Regione.objects.all()
    search_fields = ["denomination"]
    filterset_class = RegioneFilters


class ProvinciaAPIView(LengthOfDenominationROMV):
    # TIPS:
    # - use select_related() for ForeignKey and OneToOneField
    # - use prefetch_related() for ManyToManyField and reverse ForeignKey

    queryset = (
        Provincia.objects.select_related("region").prefetch_related("cities").all()
    )
    search_fields = ["denomination"]
    filterset_class = ProvinciaFilters

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProvinciaRetrieveSerializer
        return ProvinciaSerializer


class ComuneAPIView(LengthOfDenominationROMV):
    # TIPS:
    # - use select_related() for ForeignKey and OneToOneField
    # - use prefetch_related() for ManyToManyField and reverse ForeignKey

    serializer_class = ComuneSerializer
    queryset = Comune.objects.select_related("province").all()
    search_fields = ["denomination"]
    filterset_class = ComuneFilters

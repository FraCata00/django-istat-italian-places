from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from comuni_italiani.filters import ComuneFilters, ProvinciaFilters, RegioneFilters
from comuni_italiani.models import Comune, Provincia, Regione
from comuni_italiani.serializers import (
    ComuneSerializer,
    ProvinciaRetrieveSerializer,
    ProvinciaSerializer,
    RegioneSerializer,
)


# mixin
class SearchableReadOnlyViewSet(ReadOnlyModelViewSet):
    """
    A viewset that provides default `list()` and `retrieve()` actions.
    remove pagination only after search
    """

    # remove pagination only after search
    def get_paginated_response(self, data):
        if self.request.query_params.get("search"):
            return Response(data)
        return super().get_paginated_response(data)


class RegioniAPIView(SearchableReadOnlyViewSet):
    # TIPS:
    # - use select_related() for ForeignKey and OneToOneField
    # - use prefetch_related() for ManyToManyField and reverse ForeignKey

    serializer_class = RegioneSerializer
    queryset = Regione.objects.all()
    search_fields = ["denomination"]
    filterset_class = RegioneFilters


class ProvinciaAPIView(SearchableReadOnlyViewSet):
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


class ComuneAPIView(SearchableReadOnlyViewSet):
    # TIPS:
    # - use select_related() for ForeignKey and OneToOneField
    # - use prefetch_related() for ManyToManyField and reverse ForeignKey

    serializer_class = ComuneSerializer
    queryset = Comune.objects.select_related("province").all()
    search_fields = ["denomination"]
    filterset_class = ComuneFilters

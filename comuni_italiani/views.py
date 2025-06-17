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


class RegioniAPIView(ReadOnlyModelViewSet):
    # TIPS:
    # - use select_related() for ForeignKey and OneToOneField
    # - use prefetch_related() for ManyToManyField and reverse ForeignKey

    serializer_class = RegioneSerializer
    queryset = Regione.objects.all()
    search_fields = ["denomination"]
    filterset_class = RegioneFilters

    # remove pagination only after search
    def get_paginated_response(self, data):
        if self.request.query_params.get("search"):
            return Response(data)
        return super().get_paginated_response(data)


class ProvinciaAPIView(ReadOnlyModelViewSet):
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

    # remove pagination only after search
    def get_paginated_response(self, data):
        if self.request.query_params.get("search"):
            return Response(data)
        return super().get_paginated_response(data)


class ComuneAPIView(ReadOnlyModelViewSet):
    # TIPS:
    # - use select_related() for ForeignKey and OneToOneField
    # - use prefetch_related() for ManyToManyField and reverse ForeignKey

    serializer_class = ComuneSerializer
    queryset = Comune.objects.select_related("province").all()
    search_fields = ["denomination"]
    filterset_class = ComuneFilters

    # remove pagination only after search
    def get_paginated_response(self, data):
        if self.request.query_params.get("search"):
            return Response(data)
        return super().get_paginated_response(data)

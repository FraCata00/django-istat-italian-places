from django_filters import rest_framework as filters

from comuni_italiani.models import Comune, Provincia, Regione


class RegioneFilters(filters.FilterSet):
    code = filters.CharFilter(
        field_name="code",
        lookup_expr="icontains",
    )
    denomination = filters.CharFilter(
        field_name="denomination",
        lookup_expr="icontains",
    )
    geographic_partition = filters.CharFilter(
        field_name="geographic_partition",
        lookup_expr="icontains",
    )

    class Meta:
        model = Regione
        fields = ["code", "denomination", "geographic_partition"]


class ProvinciaFilters(filters.FilterSet):
    code = filters.CharFilter(
        field_name="code",
        lookup_expr="icontains",
    )
    denomination = filters.CharFilter(
        field_name="denomination",
        lookup_expr="icontains",
    )
    geographic_partition = filters.CharFilter(
        field_name="geographic_partition",
        lookup_expr="icontains",
    )
    region_id = filters.BaseInFilter(
        field_name="region",
        lookup_expr="in",
    )

    class Meta:
        model = Provincia
        fields = ["code", "denomination", "geographic_partition"]


class ComuneFilters(filters.FilterSet):
    code = filters.CharFilter(
        field_name="code",
        lookup_expr="icontains",
    )
    denomination = filters.CharFilter(
        field_name="denomination",
        lookup_expr="icontains",
    )
    geographic_partition = filters.CharFilter(
        field_name="geographic_partition",
        lookup_expr="icontains",
    )
    province_id = filters.BaseInFilter(
        field_name="province",
        lookup_expr="in",
    )
    progressive = filters.NumberFilter()

    class Meta:
        model = Comune
        fields = ["code", "denomination", "geographic_partition", "progressive"]

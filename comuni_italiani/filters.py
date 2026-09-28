from django_filters import rest_framework as filters

from comuni_italiani.models import Comune, Provincia, Regione


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    # comma-separated ids validated as numbers: a bare BaseInFilter passes the
    # raw strings to the ORM, which fails with a 500 on non-numeric input
    pass


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
    region_id = NumberInFilter(
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
    province_id = NumberInFilter(
        field_name="province",
        lookup_expr="in",
    )
    province_denomination = filters.BaseInFilter(
        field_name="province__denomination",
        lookup_expr="in",
    )
    progressive = filters.NumberFilter()

    class Meta:
        model = Comune
        fields = ["code", "denomination", "geographic_partition", "progressive"]

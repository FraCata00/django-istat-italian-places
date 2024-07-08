import logging

from rest_framework import serializers

from comuni_italiani.models import Comune, Provincia, Regione
from comuni_italiani.utils.dynamic_field_serializers import DynamicFieldsModelSerializer

logger = logging.getLogger(__name__)


class RegioneSerializer(DynamicFieldsModelSerializer):
    provinces = serializers.SerializerMethodField()
    provinces_count = serializers.IntegerField(source="provinces.count", read_only=True)

    def get_provinces(self, obj):
        return ProvinciaSerializer(
            obj.provinces.all(),
            many=True,
            fields=[
                "id",
                "code",
                "denomination",
                "geographic_partition",
                "auto_code",
            ],
        ).data

    class Meta:
        model = Regione
        fields = [
            "id",
            "code",
            "denomination",
            "geographic_partition",
            "provinces",
            "provinces_count",
        ]


class ProvinciaSerializer(DynamicFieldsModelSerializer):
    region = RegioneSerializer(
        read_only=True,
        fields=[
            "id",
            "code",
            "denomination",
            "geographic_partition",
        ],
    )

    class Meta:
        model = Provincia
        fields = [
            "id",
            "region",
            "code",
            "denomination",
            "geographic_partition",
            "auto_code",
        ]


class ComuneSerializer(DynamicFieldsModelSerializer):
    province = ProvinciaSerializer(
        read_only=True,
        fields=[
            "id",
            "code",
            "denomination",
            "geographic_partition",
            "auto_code",
        ],
    )

    class Meta:
        model = Comune
        fields = [
            "id",
            "province",
            "code",
            "progressive",
            "denomination",
            "geographic_partition",
        ]


class ProvinciaRetrieveSerializer(DynamicFieldsModelSerializer):
    region = RegioneSerializer(
        read_only=True,
        fields=[
            "id",
            "code",
            "denomination",
            "geographic_partition",
        ],
    )
    cities = ComuneSerializer(
        many=True,
        fields=[
            "id",
            "code",
            "progressive",
            "denomination",
            "geographic_partition",
        ],
    )

    class Meta:
        model = Provincia
        fields = [
            "id",
            "region",
            "code",
            "denomination",
            "geographic_partition",
            "auto_code",
            "cities",
        ]

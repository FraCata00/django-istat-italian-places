import pytest

from comuni_italiani.serializers import ProvinciaRetrieveSerializer, ProvinciaSerializer
from comuni_italiani.tests.factories import ComuneFactory, ProvinciaFactory


@pytest.mark.django_db
class TestProvinciaSerializer:
    def test_list_serializer_fields(self, provincia):
        data = ProvinciaSerializer(provincia).data
        assert set(data.keys()) == {
            "id",
            "region",
            "code",
            "denomination",
            "geographic_partition",
            "auto_code",
        }

    def test_region_nested_fields(self, provincia):
        data = ProvinciaSerializer(provincia).data
        assert set(data["region"].keys()) == {
            "id",
            "code",
            "denomination",
            "geographic_partition",
        }

    def test_dynamic_fields(self, provincia):
        data = ProvinciaSerializer(provincia, fields=["id", "code"]).data
        assert set(data.keys()) == {"id", "code"}


@pytest.mark.django_db
class TestProvinciaRetrieveSerializer:
    def test_retrieve_serializer_includes_cities(self, db):
        provincia = ProvinciaFactory()
        ComuneFactory.create_batch(3, province=provincia)
        data = ProvinciaRetrieveSerializer(provincia).data
        assert "cities" in data
        assert len(data["cities"]) == 3

    def test_cities_nested_fields(self, db):
        provincia = ProvinciaFactory()
        ComuneFactory(province=provincia)
        data = ProvinciaRetrieveSerializer(provincia).data
        city = data["cities"][0]
        assert set(city.keys()) == {
            "id",
            "code",
            "progressive",
            "denomination",
            "geographic_partition",
        }

    def test_retrieve_serializer_all_fields(self, db):
        provincia = ProvinciaFactory()
        data = ProvinciaRetrieveSerializer(provincia).data
        assert set(data.keys()) == {
            "id",
            "region",
            "code",
            "denomination",
            "geographic_partition",
            "auto_code",
            "cities",
        }

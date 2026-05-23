import pytest

from comuni_italiani.serializers import RegioneSerializer
from comuni_italiani.tests.factories import ProvinciaFactory


@pytest.mark.django_db
class TestRegioneSerializer:
    def test_contains_expected_fields(self, regione):
        data = RegioneSerializer(regione).data
        assert set(data.keys()) == {
            "id",
            "code",
            "denomination",
            "geographic_partition",
            "provinces",
            "provinces_count",
        }

    def test_dynamic_fields(self, regione):
        data = RegioneSerializer(regione, fields=["id", "code"]).data
        assert set(data.keys()) == {"id", "code"}

    def test_provinces_count_zero(self, regione):
        data = RegioneSerializer(regione).data
        assert data["provinces_count"] == 0

    def test_provinces_count_matches_related(self, regione):
        ProvinciaFactory.create_batch(3, region=regione)
        data = RegioneSerializer(regione).data
        assert data["provinces_count"] == 3

    def test_provinces_nested_fields(self, regione):
        provincia = ProvinciaFactory(region=regione)
        data = RegioneSerializer(regione).data
        assert len(data["provinces"]) == 1
        province_data = data["provinces"][0]
        assert set(province_data.keys()) == {
            "id",
            "code",
            "denomination",
            "geographic_partition",
            "auto_code",
        }
        assert province_data["id"] == provincia.pk

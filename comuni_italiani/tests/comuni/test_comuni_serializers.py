import pytest

from comuni_italiani.serializers import ComuneSerializer
from comuni_italiani.tests.factories import ComuneFactory


@pytest.mark.django_db
class TestComuneSerializer:
    def test_contains_expected_fields(self, comune):
        data = ComuneSerializer(comune).data
        assert set(data.keys()) == {
            "id",
            "province",
            "code",
            "progressive",
            "denomination",
            "geographic_partition",
        }

    def test_province_nested_fields(self, comune):
        data = ComuneSerializer(comune).data
        assert set(data["province"].keys()) == {
            "id",
            "code",
            "denomination",
            "geographic_partition",
            "auto_code",
        }

    def test_dynamic_fields(self, comune):
        data = ComuneSerializer(comune, fields=["id", "denomination"]).data
        assert set(data.keys()) == {"id", "denomination"}

    def test_progressive_value(self, db):
        comune = ComuneFactory(progressive=42)
        data = ComuneSerializer(comune).data
        assert data["progressive"] == 42

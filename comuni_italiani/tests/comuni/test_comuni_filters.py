import pytest
from django.urls import reverse

from comuni_italiani.tests.factories import ComuneFactory, ProvinciaFactory


@pytest.mark.django_db
class TestComuneFilters:
    def test_filter_by_code_icontains(self, api_client, db):
        ComuneFactory(code="000001")
        ComuneFactory(code="000002")
        response = api_client.get(reverse("comuni-list"), {"code": "000001"})
        assert response.data["count"] == 1

    def test_filter_by_denomination_icontains(self, api_client, db):
        ComuneFactory(denomination="Torino")
        ComuneFactory(denomination="Milano")
        response = api_client.get(reverse("comuni-list"), {"denomination": "Tori"})
        assert response.data["count"] == 1
        assert response.data["results"][0]["denomination"] == "Torino"

    def test_filter_by_denomination_case_insensitive(self, api_client, db):
        ComuneFactory(denomination="Torino")
        response = api_client.get(reverse("comuni-list"), {"denomination": "TORI"})
        assert response.data["count"] == 1

    def test_filter_by_geographic_partition(self, api_client, db):
        ComuneFactory(geographic_partition="Nord-Ovest")
        ComuneFactory(geographic_partition="Sud")
        response = api_client.get(reverse("comuni-list"), {"geographic_partition": "Nord"})
        assert response.data["count"] == 1

    def test_filter_by_progressive(self, api_client, db):
        ComuneFactory(progressive=10)
        ComuneFactory(progressive=20)
        response = api_client.get(reverse("comuni-list"), {"progressive": 10})
        assert response.data["count"] == 1
        assert response.data["results"][0]["progressive"] == 10

    def test_filter_by_province_id_single(self, api_client, db):
        provincia = ProvinciaFactory()
        target = ComuneFactory(province=provincia)
        ComuneFactory()
        response = api_client.get(reverse("comuni-list"), {"province_id": provincia.pk})
        assert response.data["count"] == 1
        assert response.data["results"][0]["id"] == target.pk

    def test_filter_by_province_id_multiple(self, api_client, db):
        p1 = ProvinciaFactory()
        p2 = ProvinciaFactory()
        ComuneFactory(province=p1)
        ComuneFactory(province=p2)
        ComuneFactory()
        response = api_client.get(
            reverse("comuni-list"), {"province_id": f"{p1.pk},{p2.pk}"}
        )
        assert response.data["count"] == 2

    def test_filter_by_province_denomination(self, api_client, db):
        p1 = ProvinciaFactory(denomination="Torino")
        p2 = ProvinciaFactory(denomination="Milano")
        ComuneFactory(province=p1)
        ComuneFactory(province=p2)
        response = api_client.get(
            reverse("comuni-list"), {"province_denomination": "Torino"}
        )
        assert response.data["count"] == 1

    def test_filter_no_match_returns_empty(self, api_client, db):
        ComuneFactory(denomination="Torino")
        response = api_client.get(reverse("comuni-list"), {"denomination": "Palermo"})
        assert response.data["count"] == 0

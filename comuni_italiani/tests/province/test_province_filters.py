import pytest
from django.urls import reverse

from comuni_italiani.tests.factories import ProvinciaFactory, RegioneFactory


@pytest.mark.django_db
class TestProvinciaFilters:
    def test_filter_by_code_icontains(self, api_client, db):
        ProvinciaFactory(code="001")
        ProvinciaFactory(code="002")
        response = api_client.get(reverse("province-list"), {"code": "001"})
        assert response.data["count"] == 1

    def test_filter_by_denomination_icontains(self, api_client, db):
        ProvinciaFactory(denomination="Torino")
        ProvinciaFactory(denomination="Milano")
        response = api_client.get(reverse("province-list"), {"denomination": "Tori"})
        assert response.data["count"] == 1
        assert response.data["results"][0]["denomination"] == "Torino"

    def test_filter_by_denomination_case_insensitive(self, api_client, db):
        ProvinciaFactory(denomination="Torino")
        response = api_client.get(reverse("province-list"), {"denomination": "TORI"})
        assert response.data["count"] == 1

    def test_filter_by_geographic_partition(self, api_client, db):
        ProvinciaFactory(geographic_partition="Nord-Ovest")
        ProvinciaFactory(geographic_partition="Sud")
        response = api_client.get(reverse("province-list"), {"geographic_partition": "Nord"})
        assert response.data["count"] == 1

    def test_filter_by_region_id_single(self, api_client, db):
        regione = RegioneFactory()
        target = ProvinciaFactory(region=regione)
        ProvinciaFactory()
        response = api_client.get(reverse("province-list"), {"region_id": regione.pk})
        assert response.data["count"] == 1
        assert response.data["results"][0]["id"] == target.pk

    def test_filter_by_region_id_multiple(self, api_client, db):
        r1 = RegioneFactory()
        r2 = RegioneFactory()
        ProvinciaFactory(region=r1)
        ProvinciaFactory(region=r2)
        ProvinciaFactory()
        response = api_client.get(
            reverse("province-list"), {"region_id": f"{r1.pk},{r2.pk}"}
        )
        assert response.data["count"] == 2

    def test_filter_no_match_returns_empty(self, api_client, db):
        ProvinciaFactory(denomination="Torino")
        response = api_client.get(reverse("province-list"), {"denomination": "Napoli"})
        assert response.data["count"] == 0

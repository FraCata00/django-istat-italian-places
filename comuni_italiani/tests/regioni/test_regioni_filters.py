import pytest
from django.urls import reverse

from comuni_italiani.tests.factories import RegioneFactory


@pytest.mark.django_db
class TestRegioneFilters:
    def test_filter_by_code_exact(self, api_client, db):
        RegioneFactory(code="01")
        RegioneFactory(code="02")
        response = api_client.get(reverse("regioni-list"), {"code": "01"})
        assert response.data["count"] == 1
        assert response.data["results"][0]["code"] == "01"

    def test_filter_by_code_icontains(self, api_client, db):
        RegioneFactory(code="01")
        RegioneFactory(code="02")
        response = api_client.get(reverse("regioni-list"), {"code": "0"})
        assert response.data["count"] == 2

    def test_filter_by_denomination_icontains(self, api_client, db):
        RegioneFactory(denomination="Piemonte")
        RegioneFactory(denomination="Lombardia")
        response = api_client.get(reverse("regioni-list"), {"denomination": "piem"})
        assert response.data["count"] == 1
        assert response.data["results"][0]["denomination"] == "Piemonte"

    def test_filter_by_denomination_case_insensitive(self, api_client, db):
        RegioneFactory(denomination="Piemonte")
        response = api_client.get(reverse("regioni-list"), {"denomination": "PIEM"})
        assert response.data["count"] == 1

    def test_filter_by_geographic_partition(self, api_client, db):
        RegioneFactory(geographic_partition="Nord-Ovest")
        RegioneFactory(geographic_partition="Sud")
        response = api_client.get(reverse("regioni-list"), {"geographic_partition": "Nord"})
        assert response.data["count"] == 1
        assert response.data["results"][0]["geographic_partition"] == "Nord-Ovest"

    def test_filter_no_match_returns_empty(self, api_client, db):
        RegioneFactory(denomination="Piemonte")
        response = api_client.get(reverse("regioni-list"), {"denomination": "Sardegna"})
        assert response.data["count"] == 0

import pytest
from django.urls import reverse

from comuni_italiani.tests.factories import RegioneFactory


@pytest.mark.django_db
class TestRegioniListAPI:
    def test_list_returns_200(self, api_client):
        response = api_client.get(reverse("regioni-list"))
        assert response.status_code == 200

    def test_list_contains_created_regione(self, api_client, regione):
        response = api_client.get(reverse("regioni-list"))
        ids = [r["id"] for r in response.data["results"]]
        assert regione.pk in ids

    def test_list_is_paginated(self, api_client, db):
        RegioneFactory.create_batch(5)
        response = api_client.get(reverse("regioni-list"))
        assert "results" in response.data
        assert "count" in response.data

    def test_post_not_allowed(self, api_client):
        response = api_client.post(reverse("regioni-list"), data={})
        assert response.status_code == 405

    def test_search_by_denomination(self, api_client, db):
        RegioneFactory(denomination="Piemonte")
        RegioneFactory(denomination="Lombardia")
        response = api_client.get(reverse("regioni-list"), {"search": "Piem"})
        assert response.data["count"] == 1
        assert response.data["results"][0]["denomination"] == "Piemonte"

    def test_search_orders_by_denomination_length(self, api_client, db):
        RegioneFactory(denomination="Lombardia")
        RegioneFactory(denomination="Lazio")
        response = api_client.get(reverse("regioni-list"), {"search": "La"})
        denominations = [r["denomination"] for r in response.data["results"]]
        lengths = [len(d) for d in denominations]
        assert lengths == sorted(lengths)


@pytest.mark.django_db
class TestRegioniDetailAPI:
    def test_retrieve_returns_200(self, api_client, regione):
        response = api_client.get(reverse("regioni-detail", args=[regione.pk]))
        assert response.status_code == 200

    def test_retrieve_returns_correct_data(self, api_client, regione):
        response = api_client.get(reverse("regioni-detail", args=[regione.pk]))
        assert response.data["id"] == regione.pk
        assert response.data["code"] == regione.code
        assert response.data["denomination"] == regione.denomination

    def test_retrieve_unknown_returns_404(self, api_client):
        response = api_client.get(reverse("regioni-detail", args=[9999]))
        assert response.status_code == 404

    def test_put_not_allowed(self, api_client, regione):
        response = api_client.put(reverse("regioni-detail", args=[regione.pk]), data={})
        assert response.status_code == 405

    def test_delete_not_allowed(self, api_client, regione):
        response = api_client.delete(reverse("regioni-detail", args=[regione.pk]))
        assert response.status_code == 405

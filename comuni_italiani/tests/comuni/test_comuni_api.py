import pytest
from django.urls import reverse

from comuni_italiani.tests.factories import ComuneFactory


@pytest.mark.django_db
class TestComuniListAPI:
    def test_list_returns_200(self, api_client):
        response = api_client.get(reverse("comuni-list"))
        assert response.status_code == 200

    def test_list_contains_created_comune(self, api_client, comune):
        response = api_client.get(reverse("comuni-list"))
        ids = [c["id"] for c in response.data["results"]]
        assert comune.pk in ids

    def test_list_is_paginated(self, api_client, db):
        ComuneFactory.create_batch(5)
        response = api_client.get(reverse("comuni-list"))
        assert "results" in response.data
        assert "count" in response.data

    def test_post_not_allowed(self, api_client):
        response = api_client.post(reverse("comuni-list"), data={})
        assert response.status_code == 405

    def test_search_by_denomination(self, api_client, db):
        ComuneFactory(denomination="Torino")
        ComuneFactory(denomination="Milano")
        response = api_client.get(reverse("comuni-list"), {"search": "Tori"})
        assert response.data["count"] == 1
        assert response.data["results"][0]["denomination"] == "Torino"

    def test_search_orders_by_denomination_length(self, api_client, db):
        ComuneFactory(denomination="Roma")
        ComuneFactory(denomination="Alessandria")
        response = api_client.get(reverse("comuni-list"), {"search": "a"})
        denominations = [c["denomination"] for c in response.data["results"]]
        lengths = [len(d) for d in denominations]
        assert lengths == sorted(lengths)


@pytest.mark.django_db
class TestComuniDetailAPI:
    def test_retrieve_returns_200(self, api_client, comune):
        response = api_client.get(reverse("comuni-detail", args=[comune.pk]))
        assert response.status_code == 200

    def test_retrieve_correct_data(self, api_client, comune):
        response = api_client.get(reverse("comuni-detail", args=[comune.pk]))
        assert response.data["id"] == comune.pk
        assert response.data["code"] == comune.code
        assert response.data["denomination"] == comune.denomination

    def test_retrieve_unknown_returns_404(self, api_client):
        response = api_client.get(reverse("comuni-detail", args=[9999]))
        assert response.status_code == 404

    def test_put_not_allowed(self, api_client, comune):
        response = api_client.put(reverse("comuni-detail", args=[comune.pk]), data={})
        assert response.status_code == 405

    def test_delete_not_allowed(self, api_client, comune):
        response = api_client.delete(reverse("comuni-detail", args=[comune.pk]))
        assert response.status_code == 405

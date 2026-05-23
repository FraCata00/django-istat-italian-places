import pytest
from django.urls import reverse

from comuni_italiani.tests.factories import (
    ComuneFactory,
    ProvinciaFactory,
)


@pytest.mark.django_db
class TestProvinciaListAPI:
    def test_list_returns_200(self, api_client):
        response = api_client.get(reverse("province-list"))
        assert response.status_code == 200

    def test_list_contains_created_provincia(self, api_client, provincia):
        response = api_client.get(reverse("province-list"))
        ids = [p["id"] for p in response.data["results"]]
        assert provincia.pk in ids

    def test_list_uses_list_serializer(self, api_client, provincia):
        response = api_client.get(reverse("province-list"))
        result = response.data["results"][0]
        assert "cities" not in result

    def test_post_not_allowed(self, api_client):
        response = api_client.post(reverse("province-list"), data={})
        assert response.status_code == 405

    def test_search_by_denomination(self, api_client, db):
        ProvinciaFactory(denomination="Torino")
        ProvinciaFactory(denomination="Milano")
        response = api_client.get(reverse("province-list"), {"search": "Tori"})
        assert response.data["count"] == 1
        assert response.data["results"][0]["denomination"] == "Torino"

    def test_search_orders_by_denomination_length(self, api_client, db):
        ProvinciaFactory(denomination="Roma")
        ProvinciaFactory(denomination="Alessandria")
        response = api_client.get(reverse("province-list"), {"search": "a"})
        denominations = [p["denomination"] for p in response.data["results"]]
        lengths = [len(d) for d in denominations]
        assert lengths == sorted(lengths)


@pytest.mark.django_db
class TestProvinciaDetailAPI:
    def test_retrieve_returns_200(self, api_client, provincia):
        response = api_client.get(reverse("province-detail", args=[provincia.pk]))
        assert response.status_code == 200

    def test_retrieve_uses_retrieve_serializer(self, api_client, db):
        provincia = ProvinciaFactory()
        ComuneFactory.create_batch(2, province=provincia)
        response = api_client.get(reverse("province-detail", args=[provincia.pk]))
        assert "cities" in response.data
        assert len(response.data["cities"]) == 2

    def test_retrieve_correct_data(self, api_client, provincia):
        response = api_client.get(reverse("province-detail", args=[provincia.pk]))
        assert response.data["id"] == provincia.pk
        assert response.data["code"] == provincia.code

    def test_retrieve_unknown_returns_404(self, api_client):
        response = api_client.get(reverse("province-detail", args=[9999]))
        assert response.status_code == 404

    def test_put_not_allowed(self, api_client, provincia):
        response = api_client.put(reverse("province-detail", args=[provincia.pk]), data={})
        assert response.status_code == 405

    def test_delete_not_allowed(self, api_client, provincia):
        response = api_client.delete(reverse("province-detail", args=[provincia.pk]))
        assert response.status_code == 405

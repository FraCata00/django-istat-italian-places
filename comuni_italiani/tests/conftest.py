import pytest
from rest_framework.test import APIClient

from comuni_italiani.tests.factories import (
    ComuneFactory,
    ProvinciaFactory,
    RegioneFactory,
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def regione(db):
    return RegioneFactory()


@pytest.fixture
def provincia(db):
    return ProvinciaFactory()


@pytest.fixture
def comune(db):
    return ComuneFactory()

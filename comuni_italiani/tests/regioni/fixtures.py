import pytest

from comuni_italiani.tests.factories import RegioneFactory


@pytest.fixture
def regione(db):
    yield RegioneFactory()

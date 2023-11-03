import pytest

from comuni_italiani.models import Regione


@pytest.fixture
@pytest.mark.django_db
def regione():
    yield Regione.objects.create(
        code="01",
        denomination="Piemonte",
        geographic_partition="Nord-Ovest",
    )

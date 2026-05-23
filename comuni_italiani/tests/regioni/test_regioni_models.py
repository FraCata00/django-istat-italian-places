import pytest
from django.db import IntegrityError

from comuni_italiani.tests.factories import RegioneFactory


@pytest.mark.django_db
class TestRegioneModel:
    def test_str(self, regione):
        assert str(regione) == f"Regione: {regione.denomination}"

    def test_code_is_unique(self, db):
        RegioneFactory(code="01")
        with pytest.raises(IntegrityError):
            RegioneFactory(code="01")

    def test_ordering_by_denomination(self, db):
        RegioneFactory(denomination="Zeta")
        RegioneFactory(denomination="Alpha")
        RegioneFactory(denomination="Mela")
        from comuni_italiani.models import Regione

        denominations = list(Regione.objects.values_list("denomination", flat=True))
        assert denominations == sorted(denominations)

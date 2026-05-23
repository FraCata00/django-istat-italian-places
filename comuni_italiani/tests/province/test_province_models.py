import pytest
from django.db import IntegrityError

from comuni_italiani.tests.factories import ProvinciaFactory, RegioneFactory


@pytest.mark.django_db
class TestProvinciaModel:
    def test_str(self, provincia):
        assert str(provincia) == f"Provincia: {provincia.denomination}"

    def test_code_is_unique(self, db):
        ProvinciaFactory(code="001")
        with pytest.raises(IntegrityError):
            ProvinciaFactory(code="001")

    def test_cascade_delete_from_region(self, db):
        from comuni_italiani.models import Provincia

        regione = RegioneFactory()
        ProvinciaFactory(region=regione)
        regione.delete()
        assert Provincia.objects.count() == 0

    def test_ordering_by_denomination(self, db):
        ProvinciaFactory(denomination="Torino")
        ProvinciaFactory(denomination="Alessandria")
        ProvinciaFactory(denomination="Milano")
        from comuni_italiani.models import Provincia

        denominations = list(Provincia.objects.values_list("denomination", flat=True))
        assert denominations == sorted(denominations)

    def test_auto_code_can_be_null(self, db):
        provincia = ProvinciaFactory(auto_code=None)
        assert provincia.auto_code is None

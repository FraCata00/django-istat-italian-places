import pytest
from django.db import IntegrityError

from comuni_italiani.tests.factories import ComuneFactory, ProvinciaFactory


@pytest.mark.django_db
class TestComuneModel:
    def test_str(self, comune):
        assert str(comune) == f"Comune: {comune.denomination}"

    def test_code_is_unique(self, db):
        ComuneFactory(code="000001")
        with pytest.raises(IntegrityError):
            ComuneFactory(code="000001")

    def test_cascade_delete_from_provincia(self, db):
        from comuni_italiani.models import Comune

        provincia = ProvinciaFactory()
        ComuneFactory(province=provincia)
        provincia.delete()
        assert Comune.objects.count() == 0

    def test_ordering_by_denomination(self, db):
        ComuneFactory(denomination="Torino")
        ComuneFactory(denomination="Aosta")
        ComuneFactory(denomination="Milano")
        from comuni_italiani.models import Comune

        denominations = list(Comune.objects.values_list("denomination", flat=True))
        assert denominations == sorted(denominations)

    def test_geographic_partition_can_be_null(self, db):
        comune = ComuneFactory(geographic_partition=None)
        assert comune.geographic_partition is None

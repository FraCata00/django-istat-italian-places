import pytest
from tests.regioni.fixtures import regione  # noqa: F401


class TestRegioniModel:
    @pytest.mark.django_db
    def test_regioni_srt_ok(self, regione):
        assert regione.__str__() == f"Regione: {regione.denomination}"  # noqa: F811

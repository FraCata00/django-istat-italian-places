import string

import factory
from factory.django import DjangoModelFactory

from comuni_italiani.models import Comune, Provincia, Regione

_GEO_PARTITIONS = ["Nord-Ovest", "Nord-Est", "Centro", "Sud", "Isole"]


class RegioneFactory(DjangoModelFactory):
    class Meta:
        model = Regione

    code = factory.Sequence(lambda n: f"{n + 1:02d}")
    denomination = factory.Sequence(lambda n: f"Regione {n + 1}")
    geographic_partition = factory.Iterator(_GEO_PARTITIONS)
    data = factory.LazyAttribute(lambda o: {})


class ProvinciaFactory(DjangoModelFactory):
    class Meta:
        model = Provincia

    region = factory.SubFactory(RegioneFactory)
    code = factory.Sequence(lambda n: f"{n + 1:03d}")
    denomination = factory.Sequence(lambda n: f"Provincia {n + 1}")
    geographic_partition = factory.Iterator(_GEO_PARTITIONS)
    auto_code = factory.Sequence(
        lambda n: string.ascii_uppercase[n % 26] + string.ascii_uppercase[(n // 26) % 26]
    )
    data = factory.LazyAttribute(lambda o: {})


class ComuneFactory(DjangoModelFactory):
    class Meta:
        model = Comune

    province = factory.SubFactory(ProvinciaFactory)
    code = factory.Sequence(lambda n: f"{n + 1:06d}")
    progressive = factory.Sequence(lambda n: n + 1)
    denomination = factory.Sequence(lambda n: f"Comune {n + 1}")
    geographic_partition = factory.Iterator(_GEO_PARTITIONS)
    data = factory.LazyAttribute(lambda o: {})

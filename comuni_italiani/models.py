from django.db import models

"""
Directly from ISTAT CSV file at `http://www.istat.it/storage/codici-unita-amministrative/Elenco-comuni-italiani.csv`

Permalink aggiornato: 30/06/2023
Fonte: ISTAT

Example of data GET from ISTAT:

```json
[
    {
        "Codice Regione": "01",
        "Codice dell'Unità territoriale sovracomunale \n(valida a fini statistici)": "006",
        "Codice Provincia (Storico)(1)": "006",
        "Progressivo del Comune (2)": " 160 ",
        "Codice Comune formato alfanumerico": "006160",
        "Denominazione (Italiana e straniera)": "Serravalle Scrivia",
        "Denominazione in italiano": "Serravalle Scrivia",
        "Denominazione altra lingua": "",
        "Codice Ripartizione Geografica": "1",
        "Ripartizione geografica": "Nord-ovest",
        "Denominazione Regione": "Piemonte",
        "Denominazione dell'Unità territoriale sovracomunale \n(valida a fini statistici)": "Alessandria",
        "Tipologia di Unità territoriale sovracomunale ": "1",
        "Flag Comune capoluogo di provincia/città metropolitana/libero consorzio": "0",
        "Sigla automobilistica": "AL",
        "Codice Comune formato numerico": "6160",
        "Codice Comune numerico con 110 province (dal 2010 al 2016)": "6160",
        "Codice Comune numerico con 107 province (dal 2006 al 2009)": "6160",
        "Codice Comune numerico con 103 province (dal 1995 al 2005)": "6160",
        "Codice Catastale del comune": "I657",
        "Codice NUTS1 2010": "ITC",
        "Codice NUTS2 2010 (3) ": "ITC1",
        "Codice NUTS3 2010": "ITC18",
        "Codice NUTS1 2021": "ITC",
        "Codice NUTS2 2021 (3) ": "ITC1",
        "Codice NUTS3 2021": "ITC18",
    },
    ...
]
```
"""


class Regione(models.Model):
    data = models.JSONField(default=dict)

    code = models.CharField(
        verbose_name="Codice Regione",
        max_length=50,
        help_text="Codice Regione",
        unique=True,
    )
    denomination = models.CharField(
        verbose_name="Denominazione Regione",
        max_length=255,
        help_text="Denominazione Regione",
    )
    geographic_partition = models.CharField(
        verbose_name="Ripartizione geografica",
        max_length=255,
        help_text="Ripartizione geografica",
    )

    class Meta:
        verbose_name = "Regione"
        verbose_name_plural = "Regioni"
        ordering = ["denomination"]

    def __str__(self):
        return f"Regione: {self.denomination}"


class Provincia(models.Model):
    data = models.JSONField(default=dict)

    region = models.ForeignKey(
        Regione,
        verbose_name="Regione",
        on_delete=models.CASCADE,
        related_name="provinces",
    )
    code = models.CharField(
        verbose_name="Codice Provincia (Storico)",
        max_length=50,
        help_text="Codice Provincia (Storico)",
        unique=True,
    )
    denomination = models.CharField(
        verbose_name="Denominazione Provincia",
        max_length=255,
        help_text="Denominazione Provincia",
    )
    geographic_partition = models.CharField(
        verbose_name="Ripartizione geografica",
        max_length=255,
        help_text="Ripartizione geografica",
    )
    auto_code = models.CharField(
        verbose_name="Sigla automobilistica",
        max_length=2,
        help_text="Sigla automobilistica",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Province"
        ordering = ["denomination"]

    def __str__(self):
        return f"Provincia: {self.denomination}"


class Comune(models.Models):
    data = models.JSONField(default=dict)

    province = models.ForeignKey(
        Provincia,
        verbose_name="Provincia",
        on_delete=models.CASCADE,
        related_name="cities",
    )
    code = models.CharField(
        verbose_name="Codice Comune formato alfanumerico",
        max_length=50,
        help_text="Codice Comune formato alfanumerico",
        unique=True,
    )
    progressive = models.IntegerField(
        verbose_name="Progressivo del Comune",
        help_text="Progressivo del Comune",
    )
    denomination = models.CharField(
        verbose_name="Denominazione Comune",
        max_length=255,
        help_text="Denominazione Comune",
    )
    geographic_partition = models.CharField(
        verbose_name="Ripartizione geografica",
        max_length=255,
        help_text="Ripartizione geografica",
        null=True,
    )

    class Meta:
        verbose_name = "Comune"
        verbose_name_plural = "Comuni"
        ordering = ["denomination"]

    def __str__(self):
        return f"Comune: {self.denomination}"

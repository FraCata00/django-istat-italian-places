import os
import csv
import requests

"""
Directly from ISTAT CSV file at `http://www.istat.it/storage/codici-unita-amministrative/Elenco-comuni-italiani.csv`

Permalink aggiornato: 30/06/2023
Fonte: ISTAT
Archive: `https://www.istat.it/it/archivio/6789`

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

URL = (
    "http://www.istat.it/storage/codici-unita-amministrative/Elenco-comuni-italiani.csv"
)


def download_file_csv_from_istat():
    """
    N.B. MAYBE FILE CSV SHOULD CONTAINS BAD CHARACTERS LIKE `0xe0` or any letter with accent.\n
    Must be replaced with the correct letter without accent.
    """

    local_filename = URL.split("/")[-1]
    local_filename = local_filename.lower()

    r = requests.get(URL, stream=True)

    with open(local_filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    # replace bad characters with the correct letter without accent
    with open(local_filename, "r", encoding="latin-1") as f:
        content = f.read()

        # re-write file with new encoding
        with open(local_filename, "w", encoding="utf-8") as f:
            f.write(content)

    return local_filename


# n.b. the separator is semi-colon = `;`


def get_comuni_italiani():
    """
    Get the list of all italian cities, provinces and region from ISTAT

    - The source is a CSV file at this URL: http://www.istat.it/storage/codici-unita-amministrative/Elenco-comuni-italiani.csv
    """

    csv_file = download_file_csv_from_istat()

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        comuni = [row for row in reader]

    # remove file
    os.remove(csv_file)

    return comuni

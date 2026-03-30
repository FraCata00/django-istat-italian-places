from django.db import transaction
from django.core.management.base import BaseCommand
from comuni_italiani.models import Comune, Provincia, Regione
from comuni_italiani.utils.italian_localization import get_comuni_italiani


class Command(BaseCommand):
    help = "Import data from ISTAT"

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true")

    def handle(self, *args, **options):
        if not options["force"]:
            self.stdout.write(self.style.WARNING("Are you sure? [y/N]: "))
            if input().lower() not in ["y", "yes"]:
                self.stdout.write(self.style.ERROR("Cancelled.")); return

        self.stdout.write(self.style.WARNING("Downloading ISTAT data..."))
        data_istat = get_comuni_italiani()
        total = len(data_istat)
        self.stdout.write(self.style.SUCCESS(f"Parsed {total} records"))

        with transaction.atomic():
            # --- Regions ---
            regioni_map = {}
            regioni_to_upsert = {}
            for data in data_istat:
                code = data["Codice Regione"]
                if code not in regioni_to_upsert:
                    regioni_to_upsert[code] = Regione(
                        code=code,
                        denomination=data["Denominazione Regione"],
                        geographic_partition=data["Ripartizione geografica"],
                        data=data,
                    )

            existing_regioni = {r.code: r for r in Regione.objects.all()}
            to_create, to_update = [], []
            for code, obj in regioni_to_upsert.items():
                if code in existing_regioni:
                    existing = existing_regioni[code]
                    existing.denomination = obj.denomination
                    existing.geographic_partition = obj.geographic_partition
                    existing.data = obj.data
                    to_update.append(existing)
                else:
                    to_create.append(obj)

            Regione.objects.bulk_create(to_create, ignore_conflicts=False)
            Regione.objects.bulk_update(to_update, ["denomination", "geographic_partition", "data"])

            regioni_map = {r.code: r for r in Regione.objects.all()}
            self.stdout.write(self.style.SUCCESS(f"Regioni: {len(regioni_map)}"))

            # --- Provinces ---
            province_map = {}
            province_to_upsert = {}
            for data in data_istat:
                code = data["Codice Provincia (Storico)(1)"]
                if code not in province_to_upsert:
                    province_to_upsert[code] = dict(
                        code=code,
                        denomination=data["Denominazione dell'Unità territoriale sovracomunale \n(valida a fini statistici)"],
                        geographic_partition=data["Ripartizione geografica"],
                        auto_code=data["Sigla automobilistica"],
                        data=data,
                        region=regioni_map[data["Codice Regione"]],
                    )

            existing_province = {p.code: p for p in Provincia.objects.all()}
            to_create, to_update = [], []
            for code, d in province_to_upsert.items():
                if code in existing_province:
                    p = existing_province[code]
                    for k, v in d.items():
                        setattr(p, k, v)
                    to_update.append(p)
                else:
                    to_create.append(Provincia(**d))

            Provincia.objects.bulk_create(to_create)
            Provincia.objects.bulk_update(to_update, ["denomination", "geographic_partition", "auto_code", "data", "region"])

            province_map = {p.code: p for p in Provincia.objects.all()}
            self.stdout.write(self.style.SUCCESS(f"Province: {len(province_map)}"))

            # --- Comuni ---
            existing_comuni = {c.code: c for c in Comune.objects.all()}
            to_create, to_update = [], []
            for data in data_istat:
                code = data["Codice Comune formato alfanumerico"]
                obj_data = dict(
                    code=code,
                    progressive=data["Progressivo del Comune (2)"],
                    denomination=data["Denominazione in italiano"],
                    geographic_partition=data["Ripartizione geografica"],
                    data=data,
                    province=province_map[data["Codice Provincia (Storico)(1)"]],
                )
                if code in existing_comuni:
                    c = existing_comuni[code]
                    for k, v in obj_data.items():
                        setattr(c, k, v)
                    to_update.append(c)
                else:
                    to_create.append(Comune(**obj_data))

            Comune.objects.bulk_create(to_create, batch_size=500)
            Comune.objects.bulk_update(to_update, ["progressive", "denomination", "geographic_partition", "data", "province"], batch_size=500)

            self.stdout.write(self.style.SUCCESS(f"Comuni creati: {len(to_create)}, aggiornati: {len(to_update)}"))

        self.stdout.write(self.style.SUCCESS("Import completato."))

from django.core.management.base import BaseCommand
from utils.italian_localization import get_comuni_italiani
from comuni_italiani.models import Regione, Provincia, Comune


class Command(BaseCommand):
    help = "Import data from ISTAT"

    # before launch this command, you need to specify y/N to continue
    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force import data from ISTAT",
        )

    def confirm(self, question):
        try:
            while True:
                self.stdout.write(question)
                choice = input().lower()

                if choice in ["y", "yes"]:
                    return True
                elif choice in ["n", "no"]:
                    return False
                else:
                    self.stdout.write(
                        "Please respond with 'yes' or 'no' (or 'y' or 'n').\n"
                    )
        except KeyboardInterrupt:
            self.stdout.write("\nOperation cancelled.", style_func=self.style.ERROR)
            exit(1)

    def handle(self, *args, **options):
        confirm_ = options["force"]

        if not confirm_:
            confirm = self.confirm(
                self.style.WARNING(
                    "Are you sure you want to import data from ISTAT? [y/N]: "
                )
            )

            if not confirm:
                self.stdout.write(
                    "Operation cancelled.",
                    style_func=self.style.ERROR,
                )
                exit(1)
            else:
                self.stdout.write(
                    "Operation confirmed.",
                    style_func=self.style.SUCCESS,
                )

        self.stdout.write(
            "Importing data from ISTAT",
            style_func=self.style.WARNING,
        )
        data_istat = get_comuni_italiani()

        self.stdout.write(
            "Data downloaded successfully and parsed CSV file from ISTAT",
            style_func=self.style.SUCCESS,
        )

        for i, data in enumerate(data_istat):
            # now print the progress bar in the same line
            self.stdout.write(
                "Importing Progress: {}/{}".format(i + 1, len(data_istat)),
                style_func=self.style.WARNING,
                ending="\r",
            )
            self.stdout.flush()

            # intit to parse and create Region instances
            region, _ = Regione.objects.update_or_create(
                code=data["Codice Regione"],
                defaults={
                    "denomination": data["Denominazione Regione"],
                    "geographic_partition": data["Ripartizione geografica"],
                    "data": data,
                },
            )

            # init to parse and create Provincia instances
            province, _ = Provincia.objects.update_or_create(
                code=data["Codice Provincia (Storico)(1)"],
                defaults={
                    "denomination": data[
                        "Denominazione dell'Unità territoriale sovracomunale \n(valida a fini statistici)"
                    ],
                    "geographic_partition": data["Ripartizione geografica"],
                    "auto_code": data["Sigla automobilistica"],
                    "data": data,
                    "region": region,
                },
            )

            # init to parse and create Comune instances
            Comune.objects.update_or_create(
                code=data["Codice Comune formato alfanumerico"],
                defaults={
                    "progressive": data["Progressivo del Comune (2)"],
                    "denomination": data["Denominazione in italiano"],
                    "geographic_partition": data["Ripartizione geografica"],
                    "data": data,
                    "province": province,
                },
            )

        self.stdout.write(
            "Data imported successfully",
            style_func=self.style.SUCCESS,
        )
        self.stdout.write(
            "Total Regions: {}".format(Regione.objects.count()),
            style_func=self.style.SUCCESS,
        )
        self.stdout.write(
            "Total Provinces: {}".format(Provincia.objects.count()),
            style_func=self.style.SUCCESS,
        )
        self.stdout.write(
            "Total Cities: {}".format(Comune.objects.count()),
            style_func=self.style.SUCCESS,
        )

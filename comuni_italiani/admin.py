from django.contrib import admin
from comuni_italiani.models import Regione, Provincia, Comune


@admin.register(Regione)
class RegioneAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "denomination",
        "geographic_partition",
    )
    search_fields = ["code", "denomination", "geographic_partition"]
    list_filter = [
        "denomination",
        "geographic_partition",
    ]
    fieldsets = [
        (
            "Informazioni generali",
            {
                "fields": [
                    "code",
                    "denomination",
                    "geographic_partition",
                ]
            },
        ),
    ]


@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "denomination",
        "geographic_partition",
    ]
    search_fields = [
        "code",
        "denomination",
        "geographic_partition",
        "region__denomination",
    ]
    list_filter = [
        "geographic_partition",
    ]
    fieldsets = [
        (
            "Informazioni generali",
            {
                "fields": [
                    "code",
                    "denomination",
                    "geographic_partition",
                ]
            },
        ),
        (
            "Informazioni sulla regione",
            {
                "fields": [
                    "region",
                ]
            },
        ),
    ]
    list_select_related = True
    autocomplete_fields = ["region"]


@admin.register(Comune)
class ComuneAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "denomination",
        "progressive",
    ]
    search_fields = [
        "code",
        "denomination",
        "progressive",
        "province__denomination",
        "province__region__denomination",
    ]
    list_filter = [
        "geographic_partition",
    ]
    fieldsets = [
        (
            "Informazioni generali",
            {
                "fields": [
                    "code",
                    "denomination",
                    "progressive",
                    "geographic_partition",
                ]
            },
        ),
        (
            "Informazioni sulla provincia",
            {
                "fields": [
                    "province",
                ]
            },
        ),
    ]
    list_select_related = True
    autocomplete_fields = ["province"]

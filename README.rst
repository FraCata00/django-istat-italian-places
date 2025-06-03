.. image:: https://img.shields.io/github/license/FraCata00/django-istat-italian-places
   :alt: GitHub

.. image:: https://img.shields.io/github/v/release/FraCata00/django-istat-italian-places
   :alt: GitHub release (with filter)

.. image:: https://deepwiki.com/badge.svg
   :target: https://deepwiki.com/FraCata00/django-istat-italian-places
   :alt: Ask DeepWiki

.. image:: https://img.shields.io/github/actions/workflow/status/FraCata00/django-istat-italian-places/python-publish.yml
   :alt: GitHub Workflow Status (with event)

.. image:: https://img.shields.io/github/issues/FraCata00/django-istat-italian-places
   :alt: GitHub issues

.. image:: https://github.com/FraCata00/django-istat-italian-places/workflows/CodeQL/badge.svg
  :alt: https://github.com/FraCata00/django-istat-italian-places/actions?query=workflow%3ACodeQL

===============================
Django ISTAT API italian places
===============================

Django ISTAT is a Django app to localize the ISTAT API.
The result is a Django app that you can plug into your existing Django project to localize the ISTAT API.

- The resources are: Region, Provinces and Cities.
- The data are taken from the ISTAT API (https://www.istat.it/it/archivio/6789)

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "comuni_italiani" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "comuni_italiani",
    ]

2. Include the polls URLconf in your project urls.py like this::

    path("comuni_italiani/", include("comuni_italiani.urls")),

3. Run ``python manage.py migrate`` to create the comuni_italiani models.

4. Start the development server

5. Run the management command to populate the database with the ISTAT API data::

    ``python manage.py import_istat_data``

    (If use the --force option, the command start without asking for confirmation)

6. Visit http://127.0.0.1:8000/comuni-italiani/ to view the API index.

7. Visit http://127.0.0.1:8000/comuni-italiani/regioni/ to view the API regioni.

8. Visit http://127.0.0.1:8000/comuni-italiani/province/ to view the API province.

9. Visit http://127.0.0.1:8000/comuni-italiani/comuni/ to view the API cities.

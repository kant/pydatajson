#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests del modulo pydatajson."""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import with_statement
import unittest
import nose
import pydatajson


class DataJsonTestCase(unittest.TestCase):

    def setUp(self):
        self.dj = pydatajson.DataJson()
        self.maxDiff = None

    def tearDown(self):
        del(self.dj)

    def test_is_valid_catalog_full(self):
        """Testea estructura de data.json completo bien formado."""

        res = self.dj.is_valid_catalog("tests/samples/full_data.json")
        self.assertTrue(res)

    def test_is_valid_catalog_required_fields(self):
        """ Estructura de data.json que sólo contiene campos obligatorios)."""

        res = self.dj.is_valid_catalog("tests/samples/minimum_data.json")
        self.assertTrue(res)

        res = self.dj.is_valid_catalog("tests/samples/empty_minimum_data.json")
        self.assertTrue(res)

    def test_is_valid_catalog_missing_catalog_title(self):
        """Estructura de data.json en el que un catálogo no tiene título."""

        res = self.dj.is_valid_catalog(
            "tests/samples/missing_catalog_title_data.json")
        self.assertFalse(res)

    def test_is_valid_catalog_missing_dataset_title(self):
        """Estructura de data.json en el que un dataset no tiene título."""

        res = self.dj.is_valid_catalog(
            "tests/samples/missing_dataset_title_data.json")
        self.assertFalse(res)

    def test_is_valid_catalog_missing_distribution_title(self):
        """Estructura de data.json en el que un recurso no tiene título."""

        res = self.dj.is_valid_catalog(
            "tests/samples/missing_distribution_title_data.json")
        self.assertFalse(res)

    def test_validate_catalog_full_data(self):
        """ Testea `validate_catalog` contra un data.json bien formado."""

        exp = {
            "status": "OK",
            "error": {
                "catalog": {
                    "status": "OK",
                    "title": "Datos Argentina"
                },
                "dataset": [
                    {
                        "status": "OK",
                        "title": "Sistema de contrataciones electrónicas"
                    }

                ]
            }
        }

        datajson = "tests/samples/full_data.json"
        res = self.dj.validate_catalog(datajson)
        self.assertEqual(exp, res)

    def test_validate_catalog_missing_catalog_description(self):
        """ Testea `validate_catalog` contra un data.json sin descripción de
        catálogo."""

        exp = {
            "status": "ERROR",
            "error": {
                "catalog": {
                    "status": "ERROR",
                    "title": "Título del Catálogo 1"
                },
                "dataset": [
                    {
                        "status": "OK",
                        "title": "Título del Dataset 1"
                    },
                    {
                        "status": "OK",
                        "title": "Título del Dataset 2"
                    }
                ]
            }
        }

        datajson = "tests/samples/missing_catalog_description_data.json"
        res = self.dj.validate_catalog(datajson)
        self.assertEqual(exp, res)

    def test_validate_catalog_missing_dataset_description(self):
        """ Testea `validate_catalog` contra un data.json sin descripción de
        dataset."""

        exp = {
            "status": "ERROR",
            "error": {
                "catalog": {
                    "status": "OK",
                    "title": "Título del Catálogo 1"
                },
                "dataset": [
                    {
                        "status": "ERROR",
                        "title": "Título del Dataset 1"
                    },
                    {
                        "status": "OK",
                        "title": "Título del Dataset 2"
                    }
                ]
            }
        }

        datajson = "tests/samples/missing_dataset_description_data.json"
        res = self.dj.validate_catalog(datajson)
        self.assertEqual(exp, res)

    def test_validate_catalog_multiple_missing_descriptions(self):
        """ Testea `validate_catalog` contra un data.json sin descripción de
        catálogo ni datasets (2)."""

        exp = {
            "status": "ERROR",
            "error": {
                "catalog": {
                    "status": "ERROR",
                    "title": "Título del Catálogo 1"
                },
                "dataset": [
                    {
                        "status": "ERROR",
                        "title": "Título del Dataset 1"
                    },
                    {
                        "status": "ERROR",
                        "title": "Título del Dataset 2"
                    }
                ]
            }
        }

        datajson = "tests/samples/multiple_missing_descriptions_data.json"
        res = self.dj.validate_catalog(datajson)
        self.assertEqual(exp, res)

    def test_validate_catalog_missing_distribution_title(self):
        """ Testea `validate_catalog` contra un data.json sin título en una
        distribución."""

        exp = {
            "status": "ERROR",
            "error": {
                "catalog": {
                    "status": "OK",
                    "title": ""
                },
                "dataset": [
                    {
                        "status": "ERROR",
                        "title": ""
                    }
                ]
            }
        }

        datajson = "tests/samples/missing_distribution_title_data.json"
        res = self.dj.validate_catalog(datajson)
        self.assertEqual(exp, res)

    def test_validate_catalog_missing_dataset_title(self):
        """ Testea `validate_catalog` contra un data.json sin título en un
        dataset."""

        exp = {
            "status": "ERROR",
            "error": {
                "catalog": {
                    "status": "OK",
                    "title": ""
                },
                "dataset": [
                    {
                        "status": "ERROR",
                        "title": None
                    }
                ]
            }
        }

        datajson = "tests/samples/missing_dataset_title_data.json"
        res = self.dj.validate_catalog(datajson)
        self.assertEqual(exp, res)

    def test_validate_catalog_missing_catalog_title(self):
        """ Testea `validate_catalog` contra un data.json sin título de
        catálogo."""

        exp = {
            "status": "ERROR",
            "error": {
                "catalog": {
                    "status": "ERROR",
                    "title": None
                },
                "dataset": [
                    {
                        "status": "OK",
                        "title": ""
                    }
                ]
            }
        }

        datajson = "tests/samples/missing_catalog_title_data.json"
        res = self.dj.validate_catalog(datajson)
        self.assertEqual(exp, res)

    def test_validate_catalog_remote_datajson(self):
        """ Testea `validate_catalog` contra un data.json remoto."""

        exp = {
            "status": "OK",
            "error": {
                "catalog": {
                    "status": "OK",
                    "title": "Andino Demo"
                },
                "dataset": [
                    {
                        "status": "OK",
                        "title": "Dataset Demo"
                    }
                ]
            }
        }

        datajson = "http://104.131.35.253/data.json"
        res = self.dj.validate_catalog(datajson)
        self.assertEqual(exp, res)


if __name__ == '__main__':
    nose.run(defaultTest=__name__)

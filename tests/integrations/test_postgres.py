# -*- coding: utf-8 -*-

from .. import OratorTestCase
from . import IntegrationTestCase


class PostgresIntegrationTestCase(IntegrationTestCase, OratorTestCase):
    @classmethod
    def get_manager_config(cls):
        return {
            "default": "postgres",
            "postgres": {
                "driver": "pgsql",
                "host": "localhost",
                "database": "orator_test",
                "user": "orator",
                "password": "orator",
            },
        }

    def get_marker(self):
        return "%s"

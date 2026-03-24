# -*- coding: utf-8 -*-

from .. import OratorTestCase
from . import IntegrationTestCase


class PostgresQmarkIntegrationTestCase(IntegrationTestCase, OratorTestCase):
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
                "use_qmark": True,
            },
        }

    def get_marker(self):
        return "?"

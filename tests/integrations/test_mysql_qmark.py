# -*- coding: utf-8 -*-

from .. import OratorTestCase
from . import IntegrationTestCase


class MySQLQmarkIntegrationTestCase(IntegrationTestCase, OratorTestCase):
    @classmethod
    def get_manager_config(cls):
        return {
            "default": "mysql",
            "mysql": {
                "driver": "mysql",
                "database": "orator_test",
                "user": "orator",
                "password": "orator",
                "use_qmark": True,
            },
        }

    def get_marker(self):
        return "?"

# -*- coding: utf-8 -*-

from ... import OratorTestCase
from stoobly_orator.connections import MySQLConnection
from stoobly_orator.connectors.mysql_connector import MySQLConnector
from . import IntegrationTestCase


class SchemaBuilderMySQLIntegrationTestCase(IntegrationTestCase, OratorTestCase):
    @classmethod
    def get_connection_resolver(cls):
        return DatabaseIntegrationConnectionResolver()


class DatabaseIntegrationConnectionResolver(object):

    _connection = None

    def connection(self, name=None):
        if self._connection:
            return self._connection

        self._connection = MySQLConnection(
            MySQLConnector().connect(
                {"database": "orator_test", "user": "orator", "password": "orator"}
            )
        )

        return self._connection

    def get_default_connection(self):
        return "default"

    def set_default_connection(self, name):
        pass

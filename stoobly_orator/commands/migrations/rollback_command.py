# -*- coding: utf-8 -*-

from cleo.io.inputs.option import Option
from stoobly_orator.migrations import Migrator, DatabaseMigrationRepository
from .base_command import BaseCommand


class RollbackCommand(BaseCommand):
    name = "migrate:rollback"
    description = "Rollback the last database migration."
    options = [
        Option("--database", "-d", flag=False, requires_value=True, description="The database connection to use."),
        Option("--path", "-p", flag=False, requires_value=True, description="The path of migrations files to be executed."),
        Option("--pretend", "-P", description="Dump the SQL queries that would be run."),
        Option("--force", "-f", description="Force the operation to run."),
    ]

    def _handle(self):
        if not self.confirm_to_proceed(
            "<question>Are you sure you want to rollback the last migration?:</question> "
        ):
            return

        database = self.option("database")
        repository = DatabaseMigrationRepository(self.resolver, "migrations")

        migrator = Migrator(repository, self.resolver)

        self._prepare_database(migrator, database)

        pretend = self.option("pretend")

        path = self.option("path")

        if path is None:
            path = self._get_migration_path()

        migrator.rollback(path, pretend)

        for note in migrator.get_notes():
            self.line(note)

    def _prepare_database(self, migrator, database):
        migrator.set_connection(database)

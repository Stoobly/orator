# -*- coding: utf-8 -*-

from cleo.io.inputs.option import Option
from stoobly_orator.migrations import Migrator, DatabaseMigrationRepository
from .base_command import BaseCommand


class StatusCommand(BaseCommand):
    name = "migrate:status"
    description = "Show a list of migrations up/down."
    options = [
        Option("--database", "-d", flag=False, requires_value=True, description="The database connection to use."),
        Option("--path", "-p", flag=False, requires_value=True, description="The path of migrations files to be executed."),
    ]

    def _handle(self):
        database = self.option("database")

        self.resolver.set_default_connection(database)

        repository = DatabaseMigrationRepository(self.resolver, "migrations")

        migrator = Migrator(repository, self.resolver)

        if not migrator.repository_exists():
            return self.error("No migrations found")

        self._prepare_database(migrator, database)

        path = self.option("path")

        if path is None:
            path = self._get_migration_path()

        ran = migrator.get_repository().get_ran()

        migrations = []
        for migration in migrator._get_migration_files(path):
            if migration in ran:
                migrations.append(["<fg=cyan>%s</>" % migration, "<info>Yes</>"])
            else:
                migrations.append(["<fg=cyan>%s</>" % migration, "<fg=red>No</>"])

        if migrations:
            table = self.table(["Migration", "Ran?"], migrations)
            table.render()
        else:
            return self.error("No migrations found")

        for note in migrator.get_notes():
            self.line(note)

    def _prepare_database(self, migrator, database):
        migrator.set_connection(database)

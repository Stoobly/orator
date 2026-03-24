# -*- coding: utf-8 -*-

from cleo.io.inputs.option import Option
from stoobly_orator.migrations import Migrator, DatabaseMigrationRepository
from .base_command import BaseCommand


class MigrateCommand(BaseCommand):
    name = "migrate"
    description = "Run the database migrations."
    options = [
        Option("--database", "-d", flag=False, requires_value=True, description="The database connection to use."),
        Option("--path", "-p", flag=False, requires_value=True, description="The path of migrations files to be executed."),
        Option("--seed", "-s", description="Indicates if the seed task should be re-run."),
        Option("--seed-path", flag=False, requires_value=True, description="The path of seeds files to be executed. Defaults to ./seeders."),
        Option("--pretend", "-P", description="Dump the SQL queries that would be run."),
        Option("--force", "-f", description="Force the operation to run."),
    ]

    def _handle(self):
        if not self.confirm_to_proceed(
            "<question>Are you sure you want to proceed with the migration?</question> "
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

        migrator.run(path, pretend)

        for note in migrator.get_notes():
            self.line(note)

        # If the "seed" option has been given, we will rerun the database seed task
        # to repopulate the database.
        if self.option("seed"):
            args = "--force" if self.option("force") else ""

            if database:
                args += f" --database {database}"

            if self.definition.has_option("config"):
                args += f" --config {self.option('config')}"

            if self.option("seed-path"):
                args += f" --path {self.option('seed-path')}"

            self.call("db:seed", args.strip())

    def _prepare_database(self, migrator, database):
        migrator.set_connection(database)

        if not migrator.repository_exists():
            args = ""

            if database:
                args += f"--database {database}"

            if self.definition.has_option("config"):
                args += f" --config {self.option('config')}"

            self.call("migrate:install", args.strip())

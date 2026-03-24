# -*- coding: utf-8 -*-

from cleo.io.inputs.option import Option
from .base_command import BaseCommand


class RefreshCommand(BaseCommand):
    name = "migrate:refresh"
    description = "Reset and re-run all migrations."
    options = [
        Option("--database", "-d", flag=False, requires_value=True, description="The database connection to use."),
        Option("--path", "-p", flag=False, requires_value=True, description="The path of migrations files to be executed."),
        Option("--seed", "-s", description="Indicates if the seed task should be re-run."),
        Option("--seed-path", flag=False, requires_value=True, description="The path of seeds files to be executed. Defaults to ./seeds."),
        Option("--seeder", flag=False, requires_value=True, default="database_seeder", description="The name of the root seeder."),
        Option("--force", "-f", description="Force the operation to run."),
    ]

    def _handle(self):
        if not self.confirm_to_proceed(
            "<question>Are you sure you want to refresh the database?:</question> "
        ):
            return

        database = self.option("database")

        args = "--force"

        if self.option("path"):
            args += f" --path {self.option('path')}"

        if database:
            args += f" --database {database}"

        config = self.option("config") if self.definition.has_option("config") else None
        if config:
            args += f" --config {config}"

        self.call("migrate:reset", args)

        self.call("migrate", args)

        if self._needs_seeding():
            self._run_seeder(database)

    def _needs_seeding(self):
        return self.option("seed")

    def _run_seeder(self, database):
        args = f"--seeder {self.option('seeder')} --force"

        if database:
            args += f" --database {database}"

        config = self.option("config") if self.definition.has_option("config") else None
        if config:
            args += f" --config {config}"

        if self.option("seed-path"):
            args += f" --path {self.option('seed-path')}"

        self.call("db:seed", args)

# -*- coding: utf-8 -*-

from cleo.io.inputs.option import Option
from stoobly_orator.migrations import DatabaseMigrationRepository
from .base_command import BaseCommand


class InstallCommand(BaseCommand):
    name = "migrate:install"
    description = "Create the migration repository."
    options = [
        Option("--database", "-d", flag=False, requires_value=True, description="The database connection to use."),
    ]

    def _handle(self):
        database = self.option("database")
        repository = DatabaseMigrationRepository(self.resolver, "migrations")

        repository.set_source(database)
        repository.create_repository()

        self.info("Migration table created successfully")

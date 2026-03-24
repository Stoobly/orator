# -*- coding: utf-8 -*-

import os
from cleo.io.inputs.argument import Argument
from cleo.io.inputs.option import Option
from stoobly_orator.migrations import MigrationCreator
from .base_command import BaseCommand


class MigrateMakeCommand(BaseCommand):
    name = "make:migration"
    description = "Create a new migration file."
    arguments = [
        Argument("name", required=True, description="The name of the migration."),
    ]
    options = [
        Option("--table", "-t", flag=False, requires_value=True, description="The table to create the migration for."),
        Option("--create", "-C", description="Whether the migration will create the table or not."),
        Option("--path", "-p", flag=False, requires_value=True, description="The path to migrations files."),
    ]

    needs_config = False

    def _handle(self):
        creator = MigrationCreator()

        name = self.argument("name")
        table = self.option("table")
        create = bool(self.option("create"))

        if not table and create is not False:
            table = create

        path = self.option("path")
        if path is None:
            path = self._get_migration_path()

        migration_name = self._write_migration(creator, name, table, create, path)

        self.line("<info>Created migration:</info> {}".format(migration_name))

    def _write_migration(self, creator, name, table, create, path):
        """
        Write the migration file to disk.
        """
        file_ = os.path.basename(creator.create(name, path, table, create))

        return file_

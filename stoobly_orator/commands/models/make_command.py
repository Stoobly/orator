# -*- coding: utf-8 -*-

import os
import inflection
from cleo.commands.command import Command
from cleo.io.inputs.argument import Argument
from cleo.io.inputs.option import Option
from .stubs import MODEL_DEFAULT_STUB
from ...utils import mkdir_p


class ModelMakeCommand(Command):
    name = "make:model"
    description = "Creates a new Model class."
    arguments = [
        Argument("name", required=True, description="The name of the model to create."),
    ]
    options = [
        Option("--migration", "-m", description="Create a new migration file for the model."),
        Option("--path", "-p", flag=False, requires_value=True, description="Path to models directory"),
    ]

    def handle(self):
        name = self.argument("name")
        singular = inflection.singularize(inflection.tableize(name))
        directory = self._get_path()
        filepath = self._get_path(singular + ".py")

        if os.path.exists(filepath):
            raise RuntimeError("The model file already exists.")

        mkdir_p(directory)

        parent = os.path.join(directory, "__init__.py")
        if not os.path.exists(parent):
            with open(parent, "w"):
                pass

        stub = self._get_stub()
        stub = self._populate_stub(name, stub)

        with open(filepath, "w") as f:
            f.write(stub)

        self.info("Model <comment>%s</> successfully created." % name)

        if self.option("migration"):
            table = inflection.tableize(name)

            self.call(
                "make:migration",
                f"create_{table}_table --table {table} --create",
            )

    def _get_stub(self):
        return MODEL_DEFAULT_STUB

    def _populate_stub(self, name, stub):
        stub = stub.replace("DummyClass", name)

        return stub

    def _get_path(self, name=None):
        if self.option("path"):
            directory = self.option("path")
        else:
            directory = os.path.join(os.getcwd(), "models")

        if name:
            return os.path.join(directory, name)

        return directory

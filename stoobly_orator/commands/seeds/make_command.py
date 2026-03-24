# -*- coding: utf-8 -*-

import os
import errno
import inflection
from cleo.io.inputs.argument import Argument
from cleo.io.inputs.option import Option
from ...seeds.stubs import DEFAULT_STUB
from .base_command import BaseCommand


class SeedersMakeCommand(BaseCommand):
    name = "make:seed"
    description = "Create a new seeder file."
    arguments = [
        Argument("name", required=True, description="The name of the seed."),
    ]
    options = [
        Option("--path", "-p", flag=False, requires_value=True, description="The path to seeders files. Defaults to ./seeds."),
    ]

    needs_config = False

    def _handle(self):
        # Making root seeder
        self._make("database_seeder", True)

        self._make(self.argument("name"))

    def _make(self, name, root=False):
        name = self._parse_name(name)

        path = self._get_path(name)
        if os.path.exists(path):
            if not root:
                self.error("%s already exists" % name)

            return False

        self._make_directory(os.path.dirname(path))

        with open(path, "w") as fh:
            fh.write(self._build_class(name))

        if root:
            with open(os.path.join(os.path.dirname(path), "__init__.py"), "w"):
                pass

        self.info("<fg=cyan>%s</> created successfully." % name)

    def _parse_name(self, name):
        if name.endswith(".py"):
            name = name.replace(".py", "", -1)

        return name

    def _get_path(self, name):
        """
        Get the destination class path.

        :param name: The name
        :type name: str

        :rtype: str
        """
        path = self.option("path")
        if path is None:
            path = self._get_seeders_path()

        return os.path.join(path, "%s.py" % name)

    def _make_directory(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def _build_class(self, name):
        stub = self._get_stub()
        klass = self._get_class_name(name)

        stub = stub.replace("DummyClass", klass)

        return stub

    def _get_stub(self):
        return DEFAULT_STUB

    def _get_class_name(self, name):
        return inflection.camelize(name)

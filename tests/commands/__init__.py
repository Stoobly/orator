# -*- coding: utf-8 -*-

from cleo.application import Application
from cleo.testers.command_tester import CommandTester
from .. import OratorTestCase


class OratorCommandTestCase(OratorTestCase):
    def tearDown(self):
        super().tearDown()

    def run_command(self, command, options=None):
        """
        Run the command.

        :type command: cleo.commands.command.Command
        :type options: str or None
        """
        if options is None:
            options = ""

        application = Application()
        application.add(command)

        command_tester = CommandTester(command)
        command_tester.execute(options)

        return command_tester

"""Houses all of the fixtures for the application's unit tests"""

import pytest
from click.testing import CliRunner
from app import TestConfig


@pytest.fixture
def click_runner():
    """Returns a curried runner for click tests

    The runner mus be called with the command first and the arguments second.
    """
    config = TestConfig('~/Templates')
    runner = CliRunner()

    def setup_config(cmd):
        """Function to initialize the context object

        Arguments:
            cmd (click.core.Command): The command line command to test
        """

        def arguments(args):
            """Function to load the arguments supplied to the runner

            Arguments:
                args (list): A list of argumnets to pass to the cli interface

            Returns:
                click.testing.CliRunner: Invoking the command with the
                    supplied arguments and confix

            """

            return runner.invoke(cmd, args, obj=config)
        return arguments
    return setup_config

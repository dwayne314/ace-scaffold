"""This unit test suite tests the application's "create" command.

Todo:
    - Write test for the force option when possible
"""

import os
from click.testing import CliRunner
from app.cli import create


runner = CliRunner()

def test_create_without_name():
    """An error is thrown when create is called without a name"""
    response = runner.invoke(create, [])
    assert response.exit_code == 2
    assert "Missing option '--name'" in response.output

def test_create_with_name():
    """The template's name is specified when the -n flag is applied"""
    name = "Jim"
    response = runner.invoke(create, ["-n", name])
    assert response.exit_code == 0
    assert f"Creating Template `{name}`" in response.output

def test_create_with_default_path():
    """The path defaults to the current directory if none is specified"""
    current_dir = os.getcwd()
    response = runner.invoke(create, ["-n", "Jim"])
    assert response.exit_code == 0
    assert f"{current_dir}" in response.output

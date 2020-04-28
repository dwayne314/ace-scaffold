"""This unit test suite tests the application's "clone" command."""

import os
from click.testing import CliRunner
from app.cli import clone


runner = CliRunner()

def test_clone_without_template():
    """Asserts an error is thrown when clone is called without a template"""
    response = runner.invoke(clone, [])
    assert response.exit_code == 2
    assert "Missing option '--template'" in response.output

def test_clone_with_default_name():
    """Asserts the name default is used if none is specified"""
    current_dir = os.getcwd()
    response = runner.invoke(clone, ["-t", "flask-app"])
    assert response.exit_code == 0
    assert f"{current_dir}/Untitled" in response.output

def test_clone_with_name():
    """Asserts the name default is used if none is specified"""
    current_dir = os.getcwd()
    target_dir_name = "new-project"
    response = runner.invoke(clone, ["-t", "flask-app", "-n", target_dir_name])
    assert response.exit_code == 0
    assert f"{current_dir}/{target_dir_name}" in response.output

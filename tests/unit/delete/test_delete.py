"""This unit test suite tests the application's "delete" command."""

from click.testing import CliRunner
from app.cli import delete


runner = CliRunner()

def test_delete_without_template():
    """An error is thrown when delete is called without a template"""
    response = runner.invoke(delete, [])
    assert response.exit_code == 2
    assert "Missing option '--template'" in response.output

def test_delete_with_template():
    """The template name is included in the delete message"""
    template_name = "flask-app"
    response = runner.invoke(delete, ["-t", template_name])
    assert response.exit_code == 0
    assert f"Deleting Template `{template_name}`" in response.output
 
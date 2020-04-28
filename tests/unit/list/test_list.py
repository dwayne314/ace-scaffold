"""This unit test suite tests the application's "list" command.

Todo:
    - Write tests ensuring the templates are displayed when possible

"""

from click.testing import CliRunner
from app.cli import _list


runner = CliRunner()

def test_list_templates():
    """The correct message is displayed when list is called"""
    response = runner.invoke(_list, [])
    assert response.exit_code == 0
    assert "Showing all templates" in response.output

"""This unit test suite tests the application's "delete" command."""

import pytest
from app.cli import delete


@pytest.fixture
def delete_template(click_runner):
    """Runs the delete command from the click runner"""
    return click_runner(delete)

@pytest.mark.command
@pytest.mark.delete
def test_clone_without_template(delete_template):
    """An error is thrown when clone is called without a template"""
    response = delete_template([])
    assert response.exit_code == 2
    assert "Missing option '--template'" in response.output

@pytest.mark.command
@pytest.mark.delete
def test_clone_displays_success_message(delete_template, mocker):
    """The message sent to the client from remove_template is displayed"""
    message = 'delete display message'
    mocker.patch('app.cli.remove_template', return_value={'msg': message})
    response = delete_template(["-t", "flask-app"])

    assert response.exit_code == 0
    assert message == response.output.strip()

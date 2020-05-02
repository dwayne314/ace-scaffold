"""This unit test suite tests the application's "clone" command."""

import pytest
from app.cli import clone


@pytest.fixture
def clone_template(click_runner):
    """Runs the clone command from the click runner"""
    return click_runner(clone)

@pytest.mark.command
@pytest.mark.clone
def test_clone_without_template(clone_template):
    """An error is thrown when clone is called without a template"""
    response = clone_template([])
    assert response.exit_code == 2
    assert "Missing option '--template'" in response.output

@pytest.mark.command
@pytest.mark.clone
def test_clone_displays_message(clone_template, mocker):
    """The message sent to the client from clone_template is displayed"""
    message = 'clone display message'
    mocker.patch('app.cli.clone_template', return_value={'msg': message})
    response = clone_template(["-t", "flask-app"])

    assert message == response.output.strip()

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
def test_clone_displays_success_message(clone_template, mocker):
    """The success message is sent to the client if the action is a success"""
    mocker.patch('app.cli.clone_template', return_value={'isSuccessful': True})
    template_name = 'flask-app'
    response = clone_template(["-t", "flask-app"])

    assert response.exit_code == 0
    assert f'Template `{template_name}` has been cloned' in response.output

@pytest.mark.command
@pytest.mark.clone
def test_clone_displays_failure_message(clone_template, mocker):
    """The failure message is sent to the client if the action is a failure"""
    mocker.patch('app.cli.clone_template', return_value={'isSuccessful': False})
    template_name = 'flask-app'
    response = clone_template(["-t", "flask-app"])

    assert response.exit_code == 1
    assert f'Template `{template_name}` could not be ' \
            'cloned to' in response.output

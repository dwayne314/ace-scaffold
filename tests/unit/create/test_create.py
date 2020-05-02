"""This unit test suite tests the application's "create" command."""

import pytest
from app.cli import create


@pytest.fixture
def create_template(click_runner):
    """Runs the create command from the click runner"""
    return click_runner(create)

@pytest.mark.command
@pytest.mark.create
def test_create_template_without_name(create_template):
    """An error is trhown if crate is called without a name"""
    response = create_template([])
    assert response.exit_code == 2
    assert  "Missing option '--name'" in response.output

@pytest.mark.command
@pytest.mark.create
def test_create_displays_success_message(create_template, mocker):
    """The success message is sent to the client if the action is a success"""
    mocker.patch('app.cli.create_template', return_value={'isSuccessful': True})
    template_name = 'flask-app'
    response = create_template(["-n", template_name])

    assert response.exit_code == 0
    assert f'Template `{template_name}` has been created' in response.output

@pytest.mark.command
@pytest.mark.create
def test_create_displays_failure_message(create_template, mocker):
    """The success message is sent to the client if the action is a success"""
    mocker.patch('app.cli.create_template', return_value={'isSuccessful': False})
    template_name = 'flask-app'
    response = create_template(["-n", template_name])

    assert response.exit_code == 1
    assert f'Template `{template_name}` could not be ' \
            'created' in response.output

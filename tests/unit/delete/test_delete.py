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
    """The success message is sent to the client if the delete is a success"""
    mocker.patch('app.cli.remove_template', return_value={'isSuccessful': True})
    template_name = 'flask-app'
    response = delete_template(["-t", "flask-app"])

    assert response.exit_code == 0
    assert f'Template `{template_name}` has been deleted' in response.output

@pytest.mark.command
@pytest.mark.delete
def test_clone_displays_failure_message(delete_template, mocker):
    """The failure message is sent to the client if the delete is a failure"""
    template_name = 'flask-app'
    error_message = f'Template `{template_name}` could not be deleted'
    mocker.patch(
        'app.cli.remove_template',
        return_value=dict(isSuccessful=False, error=error_message))
    response = delete_template(["-t", "flask-app"])

    assert error_message == response.output.strip()

"""This unit test suite tests the application's "list" command."""

import pytest
from app.cli import list_


@pytest.fixture
def list_templates(click_runner):
    """Runs the delete command from the click runner"""
    return click_runner(list_)

@pytest.mark.command
@pytest.mark.list
def test_list_returns_an_empty_string(list_templates):
    """An empty string is returned when there are no templates"""
    response = list_templates([])
    assert response.exit_code == 1
    assert '' is response.output

@pytest.mark.command
@pytest.mark.list
def test_list_returns_all_templates(list_templates, mocker):
    """An empty string is returned when there are no templates"""
    template_list = ['flask', 'react']
    mocker.patch('app.cli.get_templates', return_value=template_list)
    response = list_templates([])
    assert response.exit_code == 0
    assert f'1 {template_list[0]}\n2 {template_list[1]}\n' == response.output

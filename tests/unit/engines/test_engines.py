"""This unit test suite tests the application's engines."""

import os
import app.engines


def test_create_template_deletes_template_when_instructed(mocker):
    """called when get_template is True with the force flag"""
    template_name = 'flask-shell'
    template_folder = '~/templates'

    mocker.patch('os.mkdir', return_value=True)
    mocker.patch('app.engines.get_template', return_value=True)
    mocker.patch('app.engines.delete_template', return_value=True)
    app.engines.create_template(
        'src', template_name,
        {'type': 'file', "execute":lambda src, dest: src},
        True, template_folder)

    app.engines.delete_template.assert_called_once_with(
        template_name, template_folder)

def test_create_template_deletes_template_when_instructed(mocker):
    """called when get_template is True with the force flag"""
    template_name = 'flask-shell'
    template_folder = '~/templates'

    mocker.patch('os.mkdir', return_value=True)
    mocker.patch('app.engines.get_template', return_value=True)
    mocker.patch('app.engines.delete_template', return_value=True)
    create_result = app.engines.create_template(
        'src', template_name,
        {'type': 'file', "execute":lambda src, dest: src},
        False, template_folder)

    assert create_result['isSuccessful'] is False
    assert f'`{template_name}` exists. Run command with -f to override.'  \
        in create_result['error']


def test_create_template_creates_a_directory_if_type_is_file(mocker):
    """A new directory is created with the template_path and file name"""
    template_name = 'flask-shell'
    template_folder = '~/templates'
    joined_path = '~/templates/flask-shell'

    mocker.patch('os.mkdir', return_value=True)
    mocker.patch('app.engines.get_template', return_value=True)
    mocker.patch('app.engines.delete_template', return_value=True)
    mocker.patch('os.path.join', return_value=joined_path)

    app.engines.create_template(
        'src', template_name,
        {'type': 'file', "execute":lambda src, dest: src},
        True, template_folder)

    os.mkdir.assert_called_once_with(joined_path)

def test_create_template_returns_is_successful_if_file_is_created(mocker):
    """Successful is returned if the file_template_was_created"""
    template_name = 'flask-shell'
    template_folder = '~/templates'
    joined_path = '~/templates/flask-shell'

    mocker.patch('os.mkdir', return_value=True)
    mocker.patch('app.engines.get_template', return_value=True)
    mocker.patch('app.engines.delete_template', return_value=True)
    mocker.patch('os.path.join', return_value=joined_path)

    create_result = app.engines.create_template(
        'src', template_name,
        {'type': 'fiile', "execute":lambda src, dest: src},
        True, template_folder)

    assert create_result['isSuccessful'] is True

def test_create_template_does_not_create_a_directory_if_not_type_file(mocker):
    """A new directory is not created with the template_path and file name"""
    template_name = 'flask-shell'
    template_folder = '~/templates'
    joined_path = '~/templates/flask-shell'

    mocker.patch('os.mkdir', return_value=True)
    mocker.patch('app.engines.get_template', return_value=True)
    mocker.patch('app.engines.delete_template', return_value=True)
    mocker.patch('os.path.join', return_value=joined_path)

    app.engines.create_template(
        'src', template_name,
        {'type': 'directory', "execute":lambda src, dest: src},
        True, template_folder)

    assert os.mkdir.assert_not_called

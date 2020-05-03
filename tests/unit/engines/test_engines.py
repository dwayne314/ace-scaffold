"""This unit test suite tests the application's engines."""

import os
from operator import itemgetter
import pytest
import app.engines
from app.messages import ErrorMessage, InfoMessage


@pytest.fixture
def default_args():
    """Contains the default engine test arguments"""
    template_name = 'flask-shell'
    template_folder = '~/templates'
    success_status = {'is_successful': True}
    failure_status = {'is_successful': False}
    dest_path = '~/Desktop'
    clone_name = 'test'
    dest = '~/Home'

    return dict(template_name=template_name, template_folder=template_folder,
                success_status=success_status, failure_status=failure_status,
                dest_path=dest_path, clone_name=clone_name, dest=dest)

@pytest.mark.engine
def test_create_existing_template_if_not_forced(mocker, default_args):
    """calls ErrorMessage with template_exists error_type"""
    template_name, template_folder, success_status = itemgetter(
        'template_folder', 'template_folder', 'success_status')(default_args)
    force_delete = False

    mocker.patch('os.mkdir', return_value=True)
    mocker.patch('app.engines.get_template', return_value=True)
    mocker.patch('app.engines.delete_template', return_value=success_status)
    create_result = app.engines.create_template(
        'src', template_name,
        {'type': 'file', 'execute':lambda src, dest: src},
        force_delete, template_folder)

    assert create_result['is_successful'] is False
    assert create_result['msg'] == ErrorMessage(
        'template_exists', template_name=template_name).get_message()

@pytest.mark.engine
def test_create_existing_template_with_force_flag(mocker, default_args):
    """calls delete_template"""
    template_name, template_folder, success_status = itemgetter(
        'template_folder', 'template_folder', 'success_status')(default_args)
    force_delete = True

    mocker.patch('os.mkdir', return_value=True)
    mocker.patch('app.engines.get_template', return_value=True)
    mocker.patch('app.engines.delete_template', return_value=success_status)
    app.engines.create_template(
        'src', template_name,
        {'type': 'file', 'execute':lambda src, dest: success_status},
        force_delete, template_folder)

    app.engines.delete_template.assert_called_once_with(
        template_name, template_folder)

@pytest.mark.engine
def test_create_if_delete_template_throws_error(mocker, default_args):
    """calls ErrorMessage with the delete_template error type"""
    template_name, template_folder, success_status, failure_status = \
        itemgetter('template_folder', 'template_folder',
                   'success_status', 'failure_status')(default_args)
    force_delete = True

    mocker.patch('os.mkdir', return_value=True)
    mocker.patch('app.engines.get_template', return_value=True)
    mocker.patch('app.engines.delete_template', return_value=failure_status)
    create_result = app.engines.create_template(
        'src', template_name,
        {'type': 'file', 'execute':lambda src, dest: success_status},
        force_delete, template_folder)

    assert create_result['msg'] == ErrorMessage(
        'delete_template', template_name=template_name).get_message()

@pytest.mark.engine
def test_create_template_file_creates_a_directory(mocker, default_args):
    """A new directory is created with the template_path and file name"""
    template_name, template_folder, success_status = itemgetter(
        'template_folder', 'template_folder', 'success_status')(default_args)
    joined_path = '~/templates/flask-shell'

    mocker.patch('os.mkdir', return_value=True)
    mocker.patch('app.engines.get_template', return_value=True)
    mocker.patch('app.engines.delete_template', return_value=success_status)
    mocker.patch('os.path.join', return_value=joined_path)

    app.engines.create_template(
        'src', template_name,
        {'type': 'file', 'execute':lambda src, dest: success_status},
        True, template_folder)

    os.mkdir.assert_called_once_with(joined_path)

@pytest.mark.engine
def test_create_template_directory_wont_create_a_directory(
        mocker, default_args):
    """A new directory is not created with the template_path and file name"""
    template_name, template_folder, success_status, failure_status = \
        itemgetter('template_folder', 'template_folder', 'success_status',
                   'failure_status')(default_args)

    mocker.patch('os.mkdir', return_value=True)
    mocker.patch('app.engines.get_template', return_value=True)
    mocker.patch('app.engines.delete_template', return_value=success_status)

    app.engines.create_template(
        'src', template_name,
        {'type': 'directory', 'execute':lambda src, dest: failure_status},
        True, template_folder)

    assert os.mkdir.assert_not_called

@pytest.mark.engine
def test_create_template_when_clone_function_errors(mocker, default_args):
    """calls ErrorMessage with create_template error type"""
    template_name, template_folder, success_status, failure_status = \
        itemgetter('template_folder', 'template_folder', 'success_status',
                   'failure_status')(default_args)
    joined_path = '~/templates/flask-shell'

    mocker.patch('app.engines.get_template', return_value=True)
    mocker.patch('app.engines.delete_template', return_value=success_status)
    mocker.patch('os.path.join', return_value=joined_path)

    create_result = app.engines.create_template(
        'src', template_name,
        {'type': 'directory', 'execute':lambda src, dest: failure_status},
        True, template_folder)

    assert create_result['msg'] == ErrorMessage(
        'create_template', template_name=template_name).get_message()

@pytest.mark.engine
def test_create_template_with_no_errors(mocker, default_args):
    """calls InfoMessage with the template_created message type"""
    template_name, template_folder, success_status = itemgetter(
        'template_folder', 'template_folder', 'success_status')(default_args)
    joined_path = '~/templates/flask-shell'

    mocker.patch('os.mkdir', return_value=True)
    mocker.patch('app.engines.get_template', return_value=True)
    mocker.patch('app.engines.delete_template', return_value=success_status)
    mocker.patch('os.path.join', return_value=joined_path)

    create_result = app.engines.create_template(
        'src', template_name,
        {'type': 'file', 'execute':lambda src, dest: success_status},
        True, template_folder)

    assert create_result['is_successful'] is True
    assert create_result['msg'] == InfoMessage(
        'template_created', template_name=template_name).get_message()

@pytest.mark.engine
def test_clone_template_when_successful(mocker, default_args):
    """InfoMessage is called with the template_cloned message type"""
    template_name, template_folder, success_status, clone_name, dest =  \
        itemgetter(
            'template_folder', 'template_folder', 'success_status',
            'clone_name', 'dest')(default_args)
    clone_name = 'test'
    dest = '~/Home'
    dest_path = os.path.join(dest, clone_name)

    mocker.patch('app.engines.get_template', return_value=True)

    create_result = app.engines.clone_template(
        dest, template_name, clone_name,
        {'type': 'file', 'execute':lambda src, dest: success_status},
        template_folder)

    assert create_result['is_successful'] is True
    assert create_result['msg'] == InfoMessage(
        'template_cloned', path=dest_path, template_name=template_name
        ).get_message()

@pytest.mark.engine
def test_clone_template_with_path_function_error(mocker, default_args):
    """calls ErrorMessage with the clone_template error type"""
    template_name, template_folder, failure_status, clone_name, dest = \
        itemgetter(
            'template_folder', 'template_folder', 'failure_status',
            'clone_name', 'dest')(default_args)
    joined_path = '~/templates/flask-shell'

    mocker.patch('os.mkdir', return_value=True)
    mocker.patch('app.engines.get_template', return_value=True)
    mocker.patch('os.path.join', return_value=joined_path)

    create_result = app.engines.clone_template(
        dest, template_name, clone_name,
        {'type': 'file', 'execute':lambda src, dest: failure_status},
        template_folder)

    assert create_result['is_successful'] is False
    assert create_result['msg'] == ErrorMessage(
        'clone_template', template_name=template_name).get_message()

@pytest.mark.engine
def test_clone_template_does_not_exist(mocker, default_args):
    """calls ErrorMessage with the template_missing error type"""
    template_name, template_folder, clone_name = itemgetter(
        'template_name', 'template_folder', 'clone_name')(default_args)

    mocker.patch('app.engines.get_template', return_value=False)

    create_result = app.engines.clone_template(
        'dest', template_name, clone_name,
        {'type': 'file', 'execute':lambda src, dest: src},
        template_folder)

    assert create_result['is_successful'] is False
    assert create_result['msg'] == ErrorMessage(
        'template_missing', template_name=template_name).get_message()

@pytest.mark.engine
def test_delete_template_when_successful(mocker, default_args):
    """calls InfoMessage with template_deleted message type"""
    template_name, template_folder, success_status = \
        itemgetter(
            'template_name', 'template_folder',
            'success_status')(default_args)
    mocker.patch('app.engines.get_template', return_value=True)
    mocker.patch('app.engines.delete_template', return_value=success_status)
    create_result = app.engines.remove_template(
        template_name, template_folder)

    assert create_result['is_successful'] is True
    assert create_result['msg'] == InfoMessage(
        'template_deleted', template_name=template_name).get_message()

@pytest.mark.engine
def test_delete_when_delete_template_throws_error(mocker, default_args):
    """calls ErrorMessage with delete_template error type"""
    template_name, template_folder, failure_status = \
        itemgetter(
            'template_name', 'template_folder',
            'failure_status')(default_args)
    mocker.patch('app.engines.get_template', return_value=True)
    mocker.patch('app.engines.delete_template', return_value=failure_status)
    create_result = app.engines.remove_template(
        template_name, template_folder)

    assert create_result['is_successful'] is False
    assert create_result['msg'] == ErrorMessage(
        'delete_template', template_name=template_name).get_message()

@pytest.mark.engine
def test_delete_when_template_not_found(mocker, default_args):
    """calls ErrorMessage with template_missing error type"""
    template_name, template_folder = \
        itemgetter('template_name', 'template_folder')(default_args)
    mocker.patch('app.engines.get_template', return_value=False)
    create_result = app.engines.remove_template(
        template_name, template_folder)

    assert create_result['is_successful'] is False
    assert create_result['msg'] == ErrorMessage(
        'template_missing', template_name=template_name).get_message()

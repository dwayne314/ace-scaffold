"""This unit test suite tests the application's utilities."""

import shutil
import os
import pytest
from app.utils import (clone_directory, clone_file, delete_template,
                       get_template, get_clone_function)
from app.messages import ErrorMessage

@pytest.mark.utils
def test_clone_directory_with_no_errors(mocker):
    """copytree is called with src and dest and returns a success indicator"""
    mocker.patch('shutil.copytree')
    src = '~/Home'
    dest = 'test'

    clone_status = clone_directory(src, dest)
    shutil.copytree.assert_called_once_with(src, dest, symlinks=True)
    assert clone_status['is_successful'] is True

@pytest.mark.utils
def test_clone_directory_with_errors(mocker):
    """returns a failure indicator when copytree throws an OSError"""
    mocker.patch('shutil.copytree', side_effect=OSError())
    src = '~/Home'
    dest = 'test'

    clone_status = clone_directory(src, dest)
    shutil.copytree.assert_called_once_with(src, dest, symlinks=True)
    assert clone_status['is_successful'] is False

@pytest.mark.utils
def test_clone_file_with_no_errors(mocker):
    """copytree is called with src and dest and returns a success indicator"""
    mocker.patch('shutil.copy')
    src = '~/Home'
    dest = 'test'

    clone_status = clone_file(src, dest)
    shutil.copy.assert_called_once_with(src, dest)
    assert clone_status['is_successful'] is True

@pytest.mark.utils
def test_clone_file_with_errors(mocker):
    """returns a failure indicator when copytree throws an OSError"""
    mocker.patch('shutil.copy', side_effect=OSError())
    src = '~/Home'
    dest = 'test'

    clone_status = clone_file(src, dest)
    assert clone_status['is_successful'] is False

@pytest.mark.utils
def test_delete_template_removes_the_correct_template(mocker):
    """rmtree gets called on the correct template"""
    mocker.patch('shutil.rmtree')
    path = '~/Home'
    name = 'test'

    template_path = os.path.join(path, name)

    delete_status = delete_template(name, path)
    shutil.rmtree.assert_called_once_with(template_path)
    assert delete_status['is_successful'] is True

@pytest.mark.utils
def test_delete_template_with_errors(mocker):
    """returns a failure indicator when rmtree throws an OSError"""
    mocker.patch('shutil.rmtree', side_effect=OSError())
    path = '~/Home'
    name = 'test'

    delete_status = delete_template(name, path)
    assert delete_status['is_successful'] is False

@pytest.mark.utils
def test_get_template_returns_the_template_with_valid_path(mocker):
    """"get_template returns the path if the path exist"""
    valid_template_path = '~/Home'
    mocker.patch('os.path.exists', return_value=True)
    mocker.patch('os.path.join', return_value=valid_template_path)
    path = '~/Home'
    name = 'test'

    assert get_template(name, path) == valid_template_path

@pytest.mark.utils
def test_get_template_returns_the_template_with_invalid_path(mocker):
    """get_template returns False if the path doesn't exist"""
    mocker.patch('os.path.exists', return_value=False)
    path = '~/Home'
    name = 'test'

    assert get_template(name, path) is False

@pytest.mark.utils
def test_get_clone_function_if_the_path_is_a_file(mocker):
    """returns a dict with a file function and the type is file"""
    mocker.patch('os.path.isfile', return_value=True)
    mocker.patch('app.utils.clone_file', return_value='execute-file')

    clone_attributes = get_clone_function('path')
    assert clone_attributes['type'] == 'file'
    assert clone_attributes['execute']() == 'execute-file'

@pytest.mark.utils
def test_get_clone_function_if_the_path_is_a_diirectory(mocker):
    """returns a dict with a directory function and the type is directory"""
    mocker.patch('os.path.isdir', return_value=True)
    mocker.patch('app.utils.clone_directory', return_value='execute-dir')

    clone_attributes = get_clone_function('path')
    assert clone_attributes['type'] == 'directory'
    assert clone_attributes['execute']() == 'execute-dir'

@pytest.mark.utils
def test_get_clone_function_if_the_path_doesnt_exist(mocker):
    """returns a error message and error indicatot"""
    path = '~/Home'
    mocker.patch('os.path.isdir', return_value=False)
    mocker.patch('os.path.isfile', return_value=False)
    mocker.patch('app.utils.clone_directory', return_value='execute-dir')

    clone_attributes = get_clone_function(path)
    assert clone_attributes['is_successful'] is False
    assert clone_attributes['msg'] == ErrorMessage(
        'directory_missing', path=path).get_message()

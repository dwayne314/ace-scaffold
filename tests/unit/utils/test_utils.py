"""This unit test suite tests the application's utilities."""

import shutil
import os
from app.utils import (clone_directory, clone_file, delete_template,
                       get_template, get_clone_function)


def test_clone_directory(mocker):
    """copytree gets called with the correct arguments when cloning a dir"""
    mocker.patch('shutil.copytree')
    src = '~/Home'
    dest = 'test'

    clone_directory(src, dest)
    shutil.copytree.assert_called_once_with(src, dest, symlinks=True)

def test_clone_file(mocker):
    """clone gets called with the correct arguments when cloning a file"""
    mocker.patch('shutil.copy')
    src = '~/Home'
    dest = 'test'

    clone_file(src, dest)
    shutil.copy.assert_called_once_with(src, dest)

def test_delete_template_removes_the_correct_template(mocker):
    """rmtree gets called on the correct template"""
    mocker.patch('shutil.rmtree')
    path = '~/Home'
    name = 'test'

    template_path = os.path.join(path, name)

    delete_template(name, path)
    shutil.rmtree.assert_called_once_with(template_path)

def test_get_template_returns_the_template_with_valid_path(mocker):
    """"get_template returns the path if the path exist"""
    valid_template_path = '~/Home'
    mocker.patch('os.path.exists', return_value=True)
    mocker.patch('os.path.join', return_value=valid_template_path)
    path = '~/Home'
    name = 'test'

    assert get_template(name, path) == valid_template_path

def test_get_template_returns_the_template_with_invalid_path(mocker):
    """get_template returns False if the path doesn't exist"""
    mocker.patch('os.path.exists', return_value=False)
    path = '~/Home'
    name = 'test'

    assert get_template(name, path) is False


def test_get_clone_function_if_the_path_is_a_file(mocker):
    """returns a dict with a file function and the type is file"""
    mocker.patch('os.path.isfile', return_value=True)
    mocker.patch('app.utils.clone_file', return_value='execute-file')

    clone_attributes = get_clone_function('path')
    assert clone_attributes['type'] == 'file'
    assert clone_attributes['execute']() == 'execute-file'

def test_get_clone_function_if_the_path_is_a_diirectory(mocker):
    """returns a dict with a directory function and the type is directory"""
    mocker.patch('os.path.isdir', return_value=True)
    mocker.patch('app.utils.clone_directory', return_value='execute-dir')

    clone_attributes = get_clone_function('path')
    assert clone_attributes['type'] == 'directory'
    assert clone_attributes['execute']() == 'execute-dir'

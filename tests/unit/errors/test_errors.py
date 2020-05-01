"""This unit test suite tests the application's custom error classes."""

from app.errors import (ScaffoldError, InvalidOptionError,
                        TemplateNotFoundError, PathNotFoundError)


def test_scaffold_error_with_error_message():
    """ScaffoldError uses the initialized error message if one is provided"""
    try:
        raise ScaffoldError('test error')
    except ScaffoldError as err:
        assert err.message == 'test error'

def test_scaffold_error_without_error_message():
    """A default error message is used if none is provided"""
    try:
        raise ScaffoldError()
    except ScaffoldError as err:
        assert err.message == 'An uncaught error has occurred.'


def test_invalid_option_error_when_template_exists():
    """An InvalidOptionError's "option_type" message uses the provided name"""
    template_name = 'test-template'
    documented_error_option = 'template_exists'
    try:
        raise InvalidOptionError(documented_error_option, template_name)
    except ScaffoldError as err:
        assert err.message == f'Template `{template_name}` exists.' \
                               ' Run command with -f to override.'

def test_invalid_option_error_when_directory_exists():
    """An InvalidOptionError's "option_type" message uses the provided name"""
    path = '~/Home'
    documented_error_option = 'directory_exists'
    try:
        raise InvalidOptionError(
            documented_error_option, 'template_name', path)
    except ScaffoldError as err:
        assert err.message == f'Path `{path}` exists.'

def test_invalid_option_error_with_undocumented_option_type():
    """A default error message is used if the option_type is not available"""
    template_name = 'test-template'
    undocumented_error_option = 'undocumented'
    try:
        raise InvalidOptionError(undocumented_error_option, template_name)
    except ScaffoldError as err:
        assert err.message == 'An uncaught invalid option error was raised.'

def test_template_not_found_error_with_template_name():
    """The template name is added to the error message if provided"""
    template_name = 'test-template'
    try:
        raise TemplateNotFoundError(template_name)
    except ScaffoldError as err:
        assert err.message == f'Template `{template_name}` does not exist.'

def test_path_not_found_with_path():
    """The path is added to the error message when one is provided"""
    path = '~/user/Desktop'
    try:
        raise PathNotFoundError(path)
    except PathNotFoundError as err:
        assert err.message == f'Path `{path}` does not exist.'

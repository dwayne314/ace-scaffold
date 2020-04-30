"""This module contains all of the custom error classes for this app"""


class ScaffoldError(Exception):
    """The base error class for the application

    Attributes:
        message (str): the error message to display (default Something went
            wrong.)

    """

    def __init__(self, message=None, *args, **kwargs):
        self.message = message if message is not None else \
            'An uncaught error has occurred.'


class InvalidOptionError(ScaffoldError):
    """Raised when the client's action requires additional flags to succeed"

    Attributes:
        option_type (str): the type of invalid option error
        template_name (str): the name of the template causing the error

    """

    def __init__(self, option_type, template_name, *args, **kwargs):
        super(InvalidOptionError, self).__init__(*args, *kwargs, message=None)
        if option_type == 'template_exists' and template_name:
            self.message = f'Template `{template_name}` exists. Run command with -f ' \
                            'to override.'
        else:
            self.message = 'An uncaught invalid option error was raised.'


class TemplateNotFoundError(ScaffoldError):
    """Raised when the client attempts to access a template that doesn't exist"

    Attributes:
        template_name (str): the name of the template that cannot be found

    """

    def __init__(self, template_name, *args, **kwargs):
        super(TemplateNotFoundError, self).__init__(*args, *kwargs, message=None)
        self.message = f'Template `{template_name}` does not exist.'


class PathNotFoundError(ScaffoldError):
    """Raised when the client attempts to clone a path that doesn't exist"

    Attributes:
        path (str): the path that the client is attempting to clone

    """

    def __init__(self, path, *args, **kwargs):
        super(PathNotFoundError, self).__init__(*args, *kwargs, message=None)
        self.message = f'Path `{path}` does not exist.'

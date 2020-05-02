"""This module contains the Message class to handle app messages."""

import click


class Message():
    """The base class for the application messages

    Attributes:
        message_types (list): the supported message types, unsupported types
            will raise a ValueError

    Arguments:
        message_type (str): the type of message specified
        message (str): the supplied message

    """

    messsage_types = ['error', 'notification']

    def __init__(self, messsage_type, message, *args, **kwargs):

        if messsage_type not in self.messsage_types:
            raise ValueError(f'{messsage_type} is not a valid message type.')
        self.message = message

    def get_message(self):
        """Returns the instance's message"""
        return self.message


class ErrorMessage(Message):
    """Class for generating error messages

    Attributes:
        error_types (list): the supported error types

    Arguments:
        error_type (str): the type of error specified

    """

    error_types = ['template_exists', 'template_missing',
                   'directory_exists', 'directory_missing']

    def __init__(self, error_type, *args, **kwargs):
        if error_type == 'template_exists' and kwargs['template_name']:
            self.message = f'Template `{kwargs["template_name"]}` already ' \
                            'exists. Run command with -f to override.'

        if error_type == 'template_missing' and kwargs['template_name']:
            self.message = f'Template `{kwargs["template_name"]}` does not ' \
                            'exist.'

        if error_type == 'directory_exists' and kwargs['path']:
            self.message = f'Path `{kwargs["path"]}` already exists.'

        if error_type == 'directory_missing' and kwargs['path']:
            self.message = f'Path `{kwargs["path"]}` does not exist.'

        super(ErrorMessage, self).__init__(
            'error', self.message, *args, **kwargs)


class InfoMessage(Message):
    """Class for generating informational messages

    Attributes:
        message_types (list): the supported message types

    Arguments:
        messsage_type (str): the type of message specified

    """

    message_types = ['template_created', 'template-cloned']

    def __init__(self, messsage_type, *args, **kwargs):
        if messsage_type == 'template_created' and kwargs['template_name']:
            self.message = f'Template `{kwargs["template_name"]}` has been '\
                            'created.'

        if (messsage_type == 'template_cloned' and kwargs['path']
                and kwargs['template_name']):
            self.message = f'Template `{kwargs["template_name"]}` has been ' \
                           f'cloned to `{kwargs["path"]}`'

        if messsage_type == 'template_deleted' and kwargs['template_name']:
            self.message = f'Template `{kwargs["template_name"]}` has been deleted.'

        super(InfoMessage, self).__init__(
            'notification', self.message, *args, **kwargs)

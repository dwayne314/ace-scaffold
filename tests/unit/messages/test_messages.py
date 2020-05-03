"""This unit test suite tests the application's messages."""


import pytest
from app.messages import Message, ErrorMessage, InfoMessage


@pytest.mark.messages
def test_create_unsupported_message_type():
    """throws a validation error when an unsupported message is sent"""
    unsupported_message = 'unsupported_message'
    assert unsupported_message not in Message.messsage_types

    try:
        Message(unsupported_message, None)
    except ValueError as err:
        assert str(err) == f'{unsupported_message} is not a valid message ' \
                            'type.'

@pytest.mark.messages
def test_message_repr_displays_correctly():
    """Message diplays correctly"""
    message_type = 'error'
    dispatched_message = 'alert'

    message = Message(message_type, dispatched_message, None)
    assert str(message) == f'Message: {dispatched_message}'

@pytest.mark.messages
def test_create_unsupported_error_message_type():
    """throws a validation error when an unsupported error message is sent"""
    unsupported_error_type = 'unsupported_error_message'
    assert unsupported_error_type not in ErrorMessage.error_message_types

    try:
        ErrorMessage(unsupported_error_type, None)
    except ValueError as err:
        assert str(err) == f'{unsupported_error_type} is not a valid error ' \
                            'type.'

@pytest.mark.messages
def test_create_unsupported_infomessage_type():
    """throws a validation error when an unsupported info message is sent"""
    unsupported_info_type = 'unsupported_info_message'
    assert unsupported_info_type not in InfoMessage.info_message_types

    try:
        InfoMessage(unsupported_info_type, None)
    except ValueError as err:
        assert str(err) == f'{unsupported_info_type} is not a valid ' \
                            'message type.'

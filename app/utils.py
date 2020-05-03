"""This module contains the utilities used throughout the application"""

import shutil
import os
from app.messages import ErrorMessage


def clone_directory(src, dest):
    """Clones a directory from the source to the destination

    Returns:
        dict: indicates whether the clone operation threw an error

    """

    try:
        shutil.copytree(src, dest, symlinks=True)
        return {'is_successful': True}

    except OSError:
        return {'is_successful': False}

def clone_file(src, dest):
    """Clones a file from the source to the destination

    Returns:
        dict: indicates whether the clone operation threw an error

    """

    try:
        shutil.copy(src, dest)
        return {'is_successful': True}

    except OSError:
        return {'is_successful': False}

def delete_template(name, path):
    """Deletes a template

    Returns:
        dict: indicates whether the delete operation threw an error

    """
    directory = os.path.join(path, name)
    try:
        shutil.rmtree(directory)
        return {'is_successful': True}

    except OSError:
        return {'is_successful': False}

def get_template(name, path):
    """Retrieves the path of the template.

    Searches the path provided to find the name of the template.  If the
    template exists, return the name, otherwise Return False.

    Parameters:
        name (str): The name of the template.

    Returns:
        str: the path of the template if it exists.
        bool: False if the template doesn't exist.

    """

    template_path = os.path.join(path, name)
    if os.path.exists(template_path):
        return template_path
    return False

def get_clone_function(path):
    """Returns the clone function and type of a path

    Attributes:
        path (str): the path to retrieve the clone function for

    Returns:
        (dict): if successful, contains the operation status, the path type,
            and a reference to the appropriate clone function. If
            unsuccessful, returns the operation status and a message

    """

    if os.path.isfile(path):
        return {'is_successful': True, "type": "file", "execute": clone_file}

    if os.path.isdir(path):
        return {'is_successful': True, 'type': 'directory',
                'execute': clone_directory}

    message = ErrorMessage('directory_missing', path=path)
    return {'is_successful': False, 'msg': message.get_message()}

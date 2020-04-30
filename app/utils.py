"""This module contains the utilities used throughout the application"""

import shutil
import os
from app.errors import ScaffoldError, PathNotFoundError


def clone_directory(src, dest):
    """Clones a directory from the source to the destination"""
    try:
        shutil.copytree(src, dest, symlinks=True)
    except OSError as err:
        raise ScaffoldError(err)


def clone_file(src, dest):
    """Clones a file from the source to the destination"""
    try:
        shutil.copy(src, dest)
    except OSError as err:
        raise ScaffoldError(err)

def delete_template(name, path):
    """Deletes a directory"""
    directory = os.path.join(path, name)
    try:
        shutil.rmtree(directory)
    except OSError as err:
        raise ScaffoldError(directory)


def get_template(name, path):
    """Retrieves the path of the template.

    Searches the path provided to find the name of the template.  If the
    template exists, return the name, otherwise Return False.

    Parameters:
        name (str): The name of the template.

    Returns:
        template_path (str): the path of the template if it exists.
        False (Bool): if the template doesn't exist.

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
        (dict): contains the path type and a reference to the appropriate
            clone function

    Raises:
        PathNotFoundError (Exception): Thrown with the path if the path is
            invalid

    """

    if os.path.isfile(path):
        return {"type": "file", "execute": clone_file}
    if os.path.isdir(path):
        return {"type": "directory", "execute": clone_directory}
    raise PathNotFoundError(path)

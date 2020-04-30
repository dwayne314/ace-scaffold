"""This module contains all engines the app uses to operate"""

import os
from app.errors import InvalidOptionError
from app.utils import get_template, delete_template


def create_template(src, name, clone_function, force, template_folder):
    """Creates a template

    Executes the proper clone_function with the required parameters to cerate
    a template for a file or a direactory. For directories the contents are
    copied to the new template folder, while files themselves are copied to
    the new template folder. Overwriting an existing template is possible with
    the force (-f) option.

    Parameters:
        src (str): the path to create the template from
        name (str): the name of the template
        clone_function (dict): includes a type (str) and execute (func) to
            call the create the templeate with the correct parameters
        force (bool): if truthy overwrite the existing template if one exists
        template_folder (class): folder that templates currently live

    """

    new_template_dir = os.path.join(template_folder, name) \
        if clone_function['type'] == 'file' \
        else template_folder

    if get_template(name, template_folder):
        if force:
            delete_template(name, template_folder)
        else:
            try:
                raise InvalidOptionError('template_exists', name)
            except InvalidOptionError as err:
                return dict(isSuccessful=False, error=err.message, template_name=name)

    if clone_function['type'] == 'file':
        filename = os.path.basename(src)
        dest = os.path.join(new_template_dir, filename)
        os.mkdir(new_template_dir)
        clone_function['execute'](src, dest)
    else:
        dest = os.path.join(new_template_dir, name)
        clone_function['execute'](src, dest)

    return dict(isSuccessful=True, error=None, template_name=name)

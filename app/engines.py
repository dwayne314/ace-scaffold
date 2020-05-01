"""This module contains the engines that the app uses to operate.

- create_template: Creates a new template in the template_folder
- clone_template: Clones a template to the specified path

"""

import os
from app.errors import InvalidOptionError, TemplateNotFoundError
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
        template_folder (str): folder that templates currently live

    Returns:
        dict: indicates the status, an error if present, and the template name
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

def clone_template(dest, name, clone_name, path_function, template_folder):
    """Clones a template

    Clones a template to the specified directory with the specified name.
    Then builds the template's leaf node (which is the directory's leaf
    node for a directory or the file if it's a file) and clones the source
    directory to the leaf node.

    Parameters:
        dest (str): the path to clone the template to
        name (str): the name of the template
        clone_name (str): the name to call the new template
        path_function (str): a reference to the correct path function to
            execute.
        template_folder (str): the path of the templates directory

    Returns:
        dict: indicates the status, an error if present, and the template name

    """

    template_path = os.path.join(template_folder, name)
    destination_path = os.path.join(dest, clone_name)

    if not get_template(name, template_folder):
        try:
            raise TemplateNotFoundError(name)
        except TemplateNotFoundError as err:
            return dict(isSuccessful=False, error=err.message, name=name)

    path_function["execute"](template_path, destination_path)
    return dict(isSuccessful=True, error=None, name=name)

def get_templates(template_folder, search_term=''):
    """Returns all templates filtered by the search term

    Parameters:
        template_folder (str): the path of the templates directory
        search_term (str): filters the templates if the the term is present

    Returns:
        list: represents the filtered templates

    """
    return [template for template in os.listdir(template_folder)
            if search_term in template]

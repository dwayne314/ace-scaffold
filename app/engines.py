"""This module contains the engines that the app uses to operate.

- create_template: Creates a new template in the template_folder
- clone_template: Clones a template to the specified path

"""

import os
from app.utils import get_template, delete_template
from app.messages import ErrorMessage, InfoMessage


def create_template(src, name, clone_function, force, template_folder):
    """Creates a template

    Executes the proper clone_function with the scr and dest to create
    a template for a file or a directory. For directories the contents are
    copied to the new template folder, while files themselves are copied to
    the new template folder. Overwriting an existing template is possible with
    the force (-f) option.

    Parameters:
        src (str): the path to create the template from
        name (str): the name of the template
        clone_function (dict): includes a type (str) and execute (func) to
            call the create the template with the correct parameters
        force (bool): if truthy overwrite the existing template if one exists
        template_folder (str): folder that templates currently live

    Returns:
        dict: indicates the status of the operation and a result message

    """

    message = None
    is_successful = None
    message_kwargs = dict(template_name=name)

    new_template_dir = os.path.join(template_folder, name) \
        if clone_function['type'] == 'file' \
        else template_folder

    if get_template(name, template_folder):
        if force:
            delete_status = delete_template(name, template_folder)

            if not delete_status['is_successful']:
                message = ErrorMessage('delete_template', **message_kwargs)
                is_successful = False
        else:
            message = ErrorMessage('template_exists', **message_kwargs)
            is_successful = False

    if is_successful is not False:

        if clone_function['type'] == 'file':
            filename = os.path.basename(src)
            dest = os.path.join(new_template_dir, filename)
            os.mkdir(new_template_dir)
        else:
            dest = os.path.join(new_template_dir, name)

        clone_status = clone_function['execute'](src, dest)
        if clone_status['is_successful']:

            message = InfoMessage('template_created', template_name=name)
            is_successful = True
        else:
            message = ErrorMessage('create_template', template_name=name)
            is_successful = False

    return dict(is_successful=is_successful, msg=message.get_message())

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
        dict: indicates the status of the clone operation and a message

    """

    message = None
    is_successful = None
    message_kwargs = dict(template_name=name)

    src = os.path.join(template_folder, name)
    dest = os.path.join(dest, clone_name)

    if not get_template(name, template_folder):
        message = ErrorMessage('template_missing', **message_kwargs)
        is_successful = False

    if is_successful is not False:
        clone_status = path_function["execute"](src, dest)
        if clone_status['is_successful']:
            message = InfoMessage('template_cloned', path=dest,
                                  **message_kwargs)
            is_successful = True

        else:
            message = ErrorMessage('clone_template', **message_kwargs)
            is_successful = False

    return dict(is_successful=is_successful, msg=message.get_message())



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

def remove_template(template_name, template_folder):
    """Deletes the specified template

    Parameters:
        template_name (str): The name of the template to delete
        template_folder (str): the path of the templates directory

    Returns:
        dict: indicates the status of the remove operation and a message

    """

    is_successful = None
    message = None
    message_kwargs = dict(template_name=template_name)

    if get_template(template_name, template_folder):
        delete_status = delete_template(template_name, template_folder)

        if delete_status['is_successful']:
            message = InfoMessage('template_deleted', **message_kwargs)
            is_successful = True
        else:
            message = ErrorMessage('delete_template', **message_kwargs)
            is_successful = False
    else:
        message = ErrorMessage('template_missing', **message_kwargs)
        is_successful = False

    return dict(is_successful=is_successful, msg=message.get_message())

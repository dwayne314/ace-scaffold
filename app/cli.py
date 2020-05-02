"""
This module contains the command-line engine to parse incoming requests

Attributes:
    CONTEXT_SETTINGS (dict): Contains global settings for the app's context
"""

import os
import click
from app import Config
from app.utils import get_clone_function
from app.engines import (create_template, clone_template, get_templates,
                         remove_template)


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def interface(ctx):
    """SetupEnv: A simple templating program"""
    ctx.obj = Config()

@click.command(short_help="Creates a new template.")
@click.option('--name', '-n', required=True,
              help='The name to save the template as.')
@click.option('--path', '-p', required=False,
              default=os.getcwd(), type=click.Path(exists=True, readable=True),
              help='The directory to create the template from.')
@click.option('--force/--no-force', '-f', default=False,
              help='Overwrite a template if one exists.')
@click.pass_obj
def create(ctx, name, path, force):
    """Creates a template from the supplied path.

    \b
    - If no path is supplied the template is saved from the current working directory.
    - If force is supplied, and a template with that name exists it will be
        overwritten.

    """

    path_function = get_clone_function(path)
    status = create_template(path, name, path_function, force,
                             ctx.TEMPLATE_FOLDER)

    click.echo(status["msg"])

@click.command(short_help="Clones a template to a directory.")
@click.option('--template', '-t', required=True,
              help='The name of the template to clone.')
@click.option('--name', '-n', required=False,
              help='The name of the new directory.',
              default='Untitled')
@click.option('--path', '-p', required=False,
              default=os.getcwd(),
              type=click.Path(exists=False, writable=True, file_okay=False),
              help='The path to clone the template to.')
@click.pass_obj
def clone(ctx, name, path, template):
    """Clones a template to create a new environment.

    \b
    - If no name is supplied the default name "Untitled" will be used.
    - If no path is supplied the template is saved to the current working directory.
    """

    path_function = get_clone_function(path)
    status = clone_template(path, template, name, path_function,
                            ctx.TEMPLATE_FOLDER)
    click.echo(status["msg"])

@click.command(short_help="Deletes a template.")
@click.option('--template', '-t', required=True,
              help='The name of the template to delete.')
@click.pass_obj
def delete(ctx, template):
    """Deletes the specified template."""
    status = remove_template(template, ctx.TEMPLATE_FOLDER)
    click.echo(status["msg"])

@click.command(name='list', short_help="Lists all templates.")
@click.option('--filter', '-f', 'filter_', required=False,
              default='',
              help='The filter for the list.')
@click.pass_obj
def list_(ctx, filter_):
    """Displays all templates."""
    for index, template in enumerate(
            get_templates(ctx.TEMPLATE_FOLDER, filter_)):
        click.echo(f'{index + 1} {template}')

interface.add_command(create)
interface.add_command(clone)
interface.add_command(delete)
interface.add_command(list_)

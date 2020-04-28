"""
This module contains the testing and production configurations for this app

Attributes:
    BASE_DIR (str): The path that represents the app's root directory

"""

import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """The configuration object for the production environment"""
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates/')
    DEFAULT_NAME = 'Untitled'
    ENVIRONMENT = 'PRODUCTIION'


class TestConfig(Config):
    """The configuration object for the test environment

    Arguments
        TEMPLATE_FOLDER (str): the template folder for use when testing

    """

    TEMPLATE_FOLDER = None
    DEFAULT_NAME = 'Untitled'
    ENVIRONMENT = 'TESTING'

    def __init__(self, template_folder):
        super(TestConfig, self).__init__()
        self.TEMPLATE_FOLDER = template_folder

"""This module contains unit tests for the application.

There are two types of modules userd for testing:
	- Commands: the core commands that the application uses
	- Dependecies: indicates functions and utilities that the commands call

Command modules are to ensure:
    - The proper exit codes and outputs are sent to the client
    - The default arguments are properly supplied
    - The required arguments throw proper errors when not included
    - The optional arguments are properly used

Dependency modules are to ensure:
	- All errors are using the correct error messages when initialized
	- All utilities perform the correct actions with the right parameters
	- The engines call the correct functions and return the correct values

"""

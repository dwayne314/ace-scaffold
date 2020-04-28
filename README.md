Version
===
1.0

What is Ace Scaffold?
===

Ace Scaffold is a command line templating app that lets a user create and clone templates easily.

Why Ace Scaffold?
===

While developing, the most tedious and least enjoyable part of the building the application is setting up the initial project structure with boilerpalate code. While templates can be created to reduce the time spent writing boilerplate code, as my development experience grew, so did these template directories which led to additional wasted time searching for these templates. 

Features
===
Through it's arguments, Ace Scaffold will allow a user to accomplish the following:
* Create a template
* Clone a template
* Delete a template
* Display a list of all environments

Commands
===

create
---

Creates a template in the templates folder with the name "flask-project" with all files from "\~/Desktop/Tests" folder

	scaffold create -n flask-project -p ~/Desktop/Tests

Creates a template in the templates folder with the name "flask-project" with all files from the current working directory overriting the current one if it exists

	scaffold create -n flask-project -f

Creates a template in the templates folder with the name "flask-project" with all files from the current working directory

	scaffold create -n flask-project`

clone
---

Clones the flask-project template to the current working directory with the folder name "Untitled"

	scaffold clone -t flask-project

Clones the "flask-project" template to the current working directory with the folder name "web-app"

	scaffold clone -t flask-project -n web-app 

Clones the "flask-project" template to "\~/Desktop" with the folder name "web-app"

	scaffold clone -t flask-project -n web-app -p ~/Desktop 

delete
---

Deletes the flask-project from the templates directory

	scaffold delete -t flask-project

list
---

Lists all created templates

	scaffold list

Future Additions
---

* Add support for template descriptions when creating and listing templates
* Add support for cloud based templates

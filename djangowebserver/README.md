**Your APP Name Here**

This sections describes what your app does, and why was built

HTML user interface works better in Chrome and Firefox

Contacts:

Your information should be here. For example:

* Santiago Flores ( sfloresk@cisco.com )


**Container Installation**

Try to always include a container for the apps that you do. write instructions
or commands. For example:

docker run -p 8025:8025 sfloresk/nso-ui

If the container cannot be uploaded to docker hub, you can use the internal repo containers.cisco.com

**Source Installation**

Usually will be something like below:

As this is a Django application you will need to either integrate the application in your production environment or you can
get it operational in a virtual environment on your computer/server. In the distribution is a requirements.txt file that you can
use to get the package requirements that are needed. The requirements file is located in the root directory of the distribution.

It might make sense for you to create a Python Virtual Environment before installing the requirements file. For information on utilizing
a virtual environment please read http://docs.python-guide.org/en/latest/dev/virtualenvs/. Once you have a virtual environment active then
install the packages in the requirements file.

`(virtualenv) % pip install -r requirements.txt
`

To run the the application execute in the root directory of the distribution:
 - python manage.py makemigrations
 - python manage.py migrate
 - python manage.py runserver 0.0.0.0:YOUR_PORT

**Known Issues**

Write here limitations or any problem that the app can have.
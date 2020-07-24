# OSCELOT DSKTOOL

This project is a Django/Python and Learn REST replacement for the Original York DSK Building Block for Learn.

This tool may be run on youur desktop, on a remote server, or in the cloud on a PaaS of your choosing.

The DSKTOOL uses 3LO and as such requires a Learn account and use is further restricted to System Admin users only.

The DSKTOOL may be run in various free or lowcost environments.

**Note**: This is an open source community project and *is not supported or sponsored by Blackboard Inc.*

##Release Notes
###v1.0 (07/24/2020)
Supports Data Source Key and Availability status for **single** User, Course, and Enrollment Records.

**ToDo:**
  <ul>
    <li>add search and update for multiple records</li>
    <li>add Docker support</li>
    <li>add logging support</li>
    <li>add date timeboxing</li>
  </ul>
<hr>

# Installation

Prerequisiites:

You ***must*** have registered an application in your Developer Portal ([https://developer.blackboard.com](https://developer.blackboard.com)) account and added it to your Learn instance. Instructions for how to do this may be found on the [Blackboard Help site](https://help.blackboard.com)

NOTE: Make certainn to store your Key and Secret as those will be required when you install the application.

If you are intalling on Heroku yor work is nearly done - jump to the below 'Heroku' section. If installing on a local or remote server jump to the below 'Hosted' section.

### Heroku

At this time the simplest way to install and run the DSKTOOL is to use this Heroku Deploy button:
<center>
<a href="https://heroku.com/deploy">
  <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy">
</a>
</center>

You need a Heroku account but that may be created as part of the process. You may also post install optionally edit the service settings to keep youor service in sync with DSKTOOL git updates so that you are always running the latest production version!


### Hosted
You may also install DSKTOOL on you local desktop system or remote server. You may leverage 

#### Install Python 3.7.x

See https://docs.python.org/3.7/using/index.html

#### Install Django 3.x

See https://docs.djangoproject.com/en/3.0/topics/install/

#### config_template.py

Copy `config_template.py` to `config.py` and fill in your information:

```
adict = {
    "learn_rest_fqdn" : "your.learnserver.net",
    "learn_rest_key" : "Your REST API KEY GOES HERE NOT Mine",
    "learn_rest_secret" : "Your REST API SECRET GOES HEREer",
}

```

* **learn_rest_fqdn** should be set to the FQDN of your Blackboard Learn instance. Be sure to avoid the request scheme, i.e. use `mylearn.blackboard.edu`


#### To Run

* **NOTE:** The Django webserver should be made available on the public internet with a valid SSL certificate. This is recommended but not required if running on a local computer.

* **After cloning from github** run `pip install -r requirements.txt` . Next run `python manage.py migrate` to apply the migrations. And last, start the server with `python manage.py runserver`

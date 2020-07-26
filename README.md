# OSCELOT DSKTOOL

This project is a Django/Python and Learn REST replacement for the Original York DSK Building Block for Learn.

This tool may be run on youur desktop, on a remote server, or in the cloud on a PaaS of your choosing.

The DSKTOOL uses 3LO and as such requires a Learn account and use is further restricted to System Admin users only.

The DSKTOOL may be run in various free or low-cost environments.

**Note**: This is an open source community project and *is not supported or sponsored by Blackboard Inc.*

## Release Notes
### v1.0 (07/24/2020)
<ul>
  <li> Supports Data Source Key and Availability status for **single** User, Course, and Enrollment Records. </li>
  <li> Supports <b>non-SSL</b> local python and Docker Desktop deployments
</ul>

**ToDo:**
  <ul>
    <li>add SSL support to Docker deployment (coming soon!!)</li>
    <li>add search and update for multiple records</li>
    <li>add logging support</li>
    <li>add date timeboxing</li>
  </ul>
<hr>

# Installation

Prerequisiites:

You ***must*** have registered an application in your Developer Portal ([https://developer.blackboard.com](https://developer.blackboard.com)) account and added it to your Learn instance. Instructions for how to do this may be found on the [Blackboard Help site](https://help.blackboard.com)

NOTE: Make certain to store your Key and Secret as those will be required when you install the application.

SSL: DSKTOOL should be made available on the public internet with a valid SSL certificate.  For development and runtime on a local system, you may use ngrok to forward from a registered domain to the localhost:8000 with:

`~/ngrok tls -region=us -hostname=<registered_fqdn> -key ~/mydomain.rsaprivatekey.pem -crt ~/mydomain.fullchaincert.pem 8000
`

### Docker

1. Install Docker Desktop : https://www.docker.com/products/docker-desktop
1. From this project copy the docker-compose.yaml file to a directory of your choosing
1. Open a terminal and enter:
1. docker-compose up -d
1. Open your Docker Desktop Dashboard to inspect that the DSKTOOL app is running 
1. Browse to http://localhost to view the http site.



### Hosted
You may also install DSKTOOL on you local desktop system or remote server. You may leverage 

#### Install Python 3.8.x

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

* **After cloning from github** run `pip install -r requirements.txt` . Next run `python manage.py migrate` to apply the migrations. And last, start the server with `python manage.py runserver`


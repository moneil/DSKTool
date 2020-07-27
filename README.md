# OSCELOT DSKTOOL

This project is a Django/Python and Learn REST replacement for the Original York DSK Building Block for Learn.

This tool may be run on your desktop, on a remote server, or in the cloud on a PaaS of your choosing.

The DSKTOOL uses 3LO and as such requires a Learn account and use is restricted based on Learn account privileges (only Users with Admin accounts may post record updates).

**Note**: This is an open source community project and *is not supported or sponsored by Blackboard Inc.*. Pull requests welcome! Make a fork and share your work back to the project.

## Release Notes
### v1.0 (07/26/2020)
<ul>
  <li> Supports Data Source Key and Availability status for **single** User, Course, and Enrollment Records. </li>
  <li> Supports non-TLS (SSL) local python and Docker Desktop deployments
  <li> Supports TLS (SSL) deployments (see below TLS section)
</ul>

**ToDo:**
  <ul>
    <li>clean up/simplify project layout</li>
    <li>add search and update for multiple records</li>
    <li>add logging support</li>
    <li>add date timeboxing</li>
  </ul>
<hr>

# Installation

Prerequisiites:

You ***must*** have registered an application in your Developer Portal ([https://developer.blackboard.com](https://developer.blackboard.com)) account and added it to your Learn instance. 

NOTE: Make certain to store your Key and Secret as those will be required when you install the application.

### Learn
1. On your Learn instance create a user 'dsktooluser' and assign them a low, to no, privileged Institution role - I used "staff" - you may create a specific role if you choose. Do not assign a System Role. 
2. Navigate to the System Admin page and select the REST API Integrations link.
3. Enter your Application Id into the Application Id field.
2. Set the REST integration user to your 'dsktooluser'.
1. Set Available to 'Yes'.
1. Set End User Access to 'Yes'
1. Set Authorized To Act As User to 'Service Default'.
2. Click Submit.

Learn is now ready proceed with the below Docker or Hosted installation.


### Docker
Docker is likely the easiest installation at this time as it does not require any understanding of Python.

1. Install Docker Desktop : [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
1. Download the above <a id="raw-url" href="https://raw.githubusercontent.com/moneil/DSKTool/master/docker-compose.yaml" download> docker-compose.yaml </a> file to a directory of your choosing
1. Open a terminal and enter: `$ docker-compose up -d`
1. Open your Docker Desktop Dashboard to inspect that the DSKTOOL app is running 
1. Browse to http://localhost to view the http site.

### TLS
After performing the above test you can enable TLS to your local computer. 

1. Go to [https://ngrok.io](https://ngrok.com/download)
2. Sign up for a free account if you don't already have one and login
3. Download the installer for your system [https://ngrok.com/download](https://ngrok.com/download)
4. Visit [https://dashboard.ngrok.com/get-started/setup](https://dashboard.ngrok.com/get-started/setup) and copy your authtoken
5. Expand ngrok into your applications folder
6. In a terminal cd to your ngrok directory and enter `$ ./ngrok authtoken <your authtoken>`
5. Start a tunnel to the DSKTOOL Port (8000): `$ ./ngrok http 8000`
Do not close your terminal - it must stay open while you are using the TLS connection. 

You should see something like this:


> ngrok by @inconshreveable                                                    (Ctrl+C to quit)
> 
> Session Status&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;online
> 
> Account&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;your nginx username&gt; (Plan: Free)
> 
> Version&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.3.35
> 
> Region&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;United States (us)
> 
> Web Interface&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;http://127.0.0.1:4040
> 
> Forwarding&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;http://1b486ab37de2.ngrok.io -> http://localhost:8000
> 
> Forwarding&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**https://1b486ab37de2.ngrok.io -> http://localhost:8000**
> 
> Connections&nbsp;&nbsp;ttl&nbsp;&nbsp;opn&nbsp;&nbsp;rt1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;rt5&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;p50&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;p90
> 
>&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0&nbsp;&nbsp;0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.00&nbsp;&nbsp;&nbsp;0.00&nbsp;&nbsp;&nbsp;&nbsp;0.00&nbsp;&nbsp;&nbsp;&nbsp;0.00

The text in bold indicates the URL you shoud use for securely accessing and using the DSKTOOL running on your system.

**Note**: ngrok requires your terminal to be open while running. ngrok sessions do expire and will require restarting ngrok when they expire or after computer restarts etc. If ngrok is not running or has expired your browser will display the following: Tunnel `the original ngrok https url` not found. Just restart ngrok and use the new https url provided.


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


# OSCELOT DSKTOOL

This project is deprecated and should no longer be used. Please use the simpler 'one click' deployment solution over [here](https://github.com/moneil/OSCELOT-DSKTOOL-for-HEROKU) is the [OSCELOT-DSKTOOL-for-HEROKU](https://github.com/moneil/OSCELOT-DSKTOOL-for-HEROKU) project.

This project will be deleted on July 4th 2021.

This is an open source community project and *is not supported or sponsored by Blackboard Inc.*. If you find it of value please contribute! Pull requests welcome! Make a fork and share your work back to this project.

## Release Notes
### v1.0.4 (07/29/2020)
<ul>
  <li>Delete session cookie when Learn Logout link is used.</li>
  <li>Moved older release notes from app index page to here.</li>
</ul>

### v1.0.3 (07/29/2020)
<ul>
  <li>Heroku Deployable!</li>
  <li>3LO required on all pages</li>
</ul>

### v1.0.2 (07/28/2020)
<ul>
  <li>Entire site requires 3LO </li>
  <li>Strip trailing spaces from submited data</li>
  <li>Heroku work in progress</li>
  <li>Docker image updated to 1.0.2</li>
</ul>

### v1.0.1 (07/27/2020)
<ul>
  <li> Fixed django issues which were preventing correct loading </li>
  <li> Updated installation notes</li>
</ul>

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
    <li>analyze ditching Django for Flask</li>
    <li>add date timeboxing</li>
  </ul>
<hr>

# Installation

Prerequisiites:

You ***must*** have registered an application in your Developer Portal ([https://developer.blackboard.com](https://developer.blackboard.com)) account and added it to your Learn instance. 

NOTE: Make certain to store your Key and Secret as those will be required when you install the application.

### Learn
1. On your Learn instance (the same instance used in the below config steps) create a user 'dsktooluser' and assign them a low, to no, privileged Institution role - I used "staff" - you may create a specific role if you choose. Do not assign a System Role. 
2. Navigate to the System Admin page and select the REST API Integrations link.
3. Enter your Application Id into the Application Id field.
2. Set the REST integration user to your 'dsktooluser'.
1. Set Available to 'Yes'.
1. Set End User Access to 'Yes'
1. Set Authorized To Act As User to 'Service Default'.
2. Click Submit.

Learn is now ready proceed with the below Docker or Hosted installation.

### Install on Your Local Computer...
First you will install support for TLS using ngrok, then you will install Docker and run your edited version of the project docker-compose.yaml file.

#### TLS
TLS support is provided by ngrok which provides a TSL tunnel to the DSKTOOL running on to your local computer. 

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


### Docker
Docker is likely the easiest installation at this time as it does not require any understanding of Python.

1. Install Docker Desktop : [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
1. Download the above <a id="raw-url" href="https://raw.githubusercontent.com/moneil/DSKTool/master/docker-compose.yaml" download> docker-compose.yaml </a> file to a directory of your choosing
2. Open the docker-compose.yaml file and edit the following:

    ````
    DJANGO_SECRET_KEY: 'secret from above generator'

    BLACKBOARD\_LEARN\_INSTANCE: "your Learn FQDN no protocol e.g. my.learn.server.com"
   
    APPLICATION\_KEY: "your application key"

    APPLICATIONN\_SECRET: "your application secret"
    ````
   Note if you want to always run the latest image you may also edit: 
   
   image: blackboardhub.ddns.net/bbdn/oscelot-dsktool:1.0 
   and replace 1.0 with the latest version indicated in this site's docker-compose.yaml file.

4. Open a terminal, cd to the directory where you saved the docker-compose.yaml file and enter: `$ docker-compose up -d`

  If you changed the file name you would use `$ docker-compose -f <your filename> up -d`
  
1. Open your Docker Desktop Dashboard to inspect that the DSKTOOL app is running 
2. Log out of Learn
1. Browse to https URL provided by ngrok and click the whoami link to view the https site and ensure the site is functioning. You should be asked to login to the configured Learn instance.

#### Oopsies
If for some reason you get an error loading the site there are a few things to check:

* Ensure the tool is properly installed in Learn
* Ensure you changed the DJANGO_SECRET_KEY and that it is enclosed by single quotes this is important.
* If you see an error similar to the one below - check your compose file syntax - esp those gnnarly double and single quotes:

>     ERROR: yaml.parser.ParserError: while parsing a block mapping
>         in "./docker-compose.yaml", line 14, column 13
>     expected <block end>, but found '<scalar>'
>         in "./docker-compose.yaml", line 16, column 34


* Refresh your DSKTOOL image by purging the current one:

```
    1. Using your terminal enter $ docker image ls
       you should see something like this:
       REPOSITORY                                   TAG   IMAGE ID
       blackboardhub.ddns.net/bbdn/oscelot-dsktool  1.0   ec77fd2d0003
       
    2. run $ docker image rm ec77fd2d0003 substituting your image id
       This deletes the cached image so when you run docker-compose next it will pull a fresh copy.
```

Rerun docker-compose.yaml to pull the new image and deploy the container.


### Hosted
You may also install DSKTOOL on your local desktop system or remote server. It is recommended that you use a python virtual environment such as pyenv.

#### Clone the repo
1. Change to your development directory
2. Clone the repository:
`git clone https://github.com/moneil/DSKTool dsktool.git`

#### Install Python 3.8.x

See https://docs.python.org/3.8/using/index.html

#### Install Django 3.x

See https://docs.djangoproject.com/en/3.0/topics/install/

#### config_template.py

Use https://djskgen.herokuapp.com to generate a django_secret_key

Copy `config_template.py` to `config.py` and fill in your information:

```
adict = {
    "learn_rest_fqdn" : "your.learnserver.net",
    "learn_rest_key" : "Your REST API KEY GOES HERE NOT Mine",
    "learn_rest_secret" : "Your REST API SECRET GOES HERE",
    "django_secret_key" : 'a secret key from the above URL',
    "django_allowed_hosts" : "127.0.0.1 localhost .ngrok.io .herokuapp.com [::1]"
    }

```

* **learn\_rest\_fqdn** should be set to the FQDN of your Blackboard Learn instance. E.g. use `mylearn.blackboard.edu`


#### To Run
You should have TLS setup - follow the above ngrok installation or set up your own cert by:
`$ pip install django-extensions`

`$ pip install Werkzeug`

`$ pip install pyOpenSSL`

`pip freeze -r requirements.txt`

Generate your cert - see: https://devcenter.heroku.com/articles/ssl-certificate-self 

or use a purchased cert

Finally add 'django_extensions' to INSTALLED\_APPS in the settings.py

After you create and edit your config.py file in the next step you may then run: python manage.py runserver_plus --cert certname

* **If Using ngrok** run `pip install -r requirements.txt` . Next run `python manage.py migrate` to apply the migrations. And last, start the server with `python manage.py runserver`
* **If Using your own cert** run `$ python manage.py runserver_plus --cert certname`



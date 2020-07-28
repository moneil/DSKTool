# Config.py DO NOT CHECK THIS INTO A PUBLICLY VIEWABLE GIT REPO!!!
# Copy to config.py. Modify values with what you got from 
# your REST App registration on developer.blackboard.com
# Use:
# from config import adict
# KEY = adict['learn_rest_key']
# SECRET = adict['learn_rest_key']
# LEARNFQDN = adict['learn_rest_fqdn']
# django_secret_key comes from here: https://djskgen.herokuapp.com

adict = {
    "learn_rest_fqdn" : "your.learnserver.net",
    "learn_rest_key" : "Your REST API KEY GOES HERE NOT Mine",
    "learn_rest_secret" : "Your REST API SECRET GOES HEREer",
    "django_secret_key" : 'a secret key from the above URL',
    "django_allowed_hosts" : "127.0.0.1 localhost .ngrok.io .herokuapp.com [::1]"
}


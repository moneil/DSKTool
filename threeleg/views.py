from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.urls import reverse
import bbrest
from bbrest import BbRest
import jsonpickle
import json
import os


try:
    print("using config.py...")
    from config import adict


    KEY = adict['learn_rest_key']
    SECRET = adict['learn_rest_secret']
    LEARNFQDN = adict['learn_rest_fqdn']

except:
    print("using Heroku env settings...")
    KEY = os.environ.get('APPLICATION_KEY', '')
    SECRET = os.environ.get('APPLICATION_SECRET', '')
    TARGET_URL = os.environ.get('BLACKBOARD_LEARN_INSTANCE', '')


# Create your views here.

def isup(request):
    return render(request, 'isup.html')
    
def index(request):
    """View function for home page of site."""

    # The following gets/stores the object to access Learn in the user's session.
    # This is key for 3LO web applications so that when you use the app, your
    # session has your object for accessing 
    bb = BbRest(KEY, SECRET, f"https://{LEARNFQDN}" )
    resp = bb.GetVersion()
    version_json = resp.json()

    context = {
        'learn_server': LEARNFQDN,
        'version_json' : version_json,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def whoami(request):
    """View function for whoami page of site."""
    bb_json = request.session.get('bb_json')
    if (bb_json is None):
        bb = BbRest(KEY, SECRET, f"https://{LEARNFQDN}" )
        bb_json = jsonpickle.encode(bb)
        print('pickled BbRest putting it on session')
        request.session['bb_json'] = bb_json
        request.session['target_view'] = 'whoami' # So after we have the access token we know to come back here.
        # The following does maintain the https: scheme if that was used with the incomming request.
        # BUT because I'm terminating the tls at the ngrok server, my incomming request is http.
        # Hence the redirect to get_auth_code is http in development. But we want our redirect_uri to be
        # have a scheme of https so that the Learn server can redirect back through ngrok with our 
        # secure SSL cert. We'll have to build a redirect_uri with the https scheme in the 
        # get_auth_code function.
        return HttpResponseRedirect(reverse('get_auth_code'))
    else:
        print('got BbRest from session')
        bb = jsonpickle.decode(bb_json)
        if bb.is_expired():
            print('expired token')
            request.session['bb_json'] = None
            whoami(request)
        bb.supported_functions() # This and the following are required after
        bb.method_generator()    # unpickling the pickled object.
        print(f'expiration: {bb.expiration()}')

    resp = bb.call('GetUser', userId = "me", params = {'fields':'id, userName, name.given, name.middle, name.family, externalId, contact.email, dataSourceId, created'}, sync=True ) #Need BbRest to support "me"
    
    user_json = resp.json()

    dskresp = bb.call('GetDataSource', dataSourceId = user_json['dataSourceId'], sync=True)
    dsk_json = dskresp.json()

    user_json['dataSourceId'] = dsk_json['externalId']

    context = {
        'user_json': user_json,
        'access_token': bb.token_info['access_token']
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'whoami.html', context=context)

def courses(request):
    task = request.GET.get('task')
    searchBy = request.GET.get('searchBy')
    searchValue = request.GET.get('searchValue')
    print ("SEARCHBY: ", searchBy)
    print ("SEARCHVALUE: ", searchValue)
    print ("TASK: ", task)

    bb_json = request.session.get('bb_json')
    if (bb_json is None):
        bb = BbRest(KEY, SECRET, f"https://{LEARNFQDN}" )
        bb_json = jsonpickle.encode(bb)
        print('pickled BbRest putting it on session')
        request.session['bb_json'] = bb_json
        request.session['target_view'] = 'courses'
        return HttpResponseRedirect(reverse('get_auth_code'))
    else:
        print('got BbRest from session')
        bb = jsonpickle.decode(bb_json)
        if bb.is_expired():
            print('expired token')
            request.session['bb_json'] = None
            whoami(request)
        bb.supported_functions() # This and the following are required after
        bb.method_generator()    # unpickling the pickled object.
        print(f'expiration: {bb.expiration()}')

    if (task == 'search'):
        #Process request...
        print (f"COURSE REQUEST: ACTION {task}")
        searchValue = request.GET.get('searchValue')
        print (f"COURSE REQUEST: CRS: {searchValue}")
        print (f"Process by {searchBy}")
        if (searchBy == 'externalId'):
            crs="externalId:" + searchValue
            print(f"course pattern: {crs}")
        elif (searchBy == 'primaryId'):
            crs=searchValue
            print(f"course pattern: {crs}")
        elif (searchBy == 'courseId'):
            crs="courseId:" + searchValue
            print(f"course pattern: {crs}")
        resp = bb.GetCourse(courseId = crs, params = {'fields':'id, courseId, externalId, name, availability.available, dataSourceId, created'}, sync=True )
        if (resp.status_code == 200):
            course_json = resp.json() 
            dskresp = bb.GetDataSource(dataSourceId = course_json['dataSourceId'], sync=True)
            dsk_json = dskresp.json()
            course_json['dataSourceId'] = dsk_json['externalId']
            course_json['searchValue'] = searchValue
            course_json['searchBy'] = searchBy
            dskresp = bb.GetDataSources(params={'fields':'id, externalId'}, sync=True)
            dsks_json = dskresp.json()
            print ("DSKS:\n", dsks_json["results"])
            dsks = dsks_json["results"]
            dsks = sortDsk(dsks)
            print ("SIZE OF DSK LIST:", len(dsks))
                
            context = {
              'course_json': course_json,
              'dsks_json': dsks,
            }
        else:
            error_json = resp.json()
            print (f"RESPONSE:\n", error_json)
            context = {
                'error_json': error_json,
            }

        return render(request, 'courses.html', context=context)

    if (task == 'process'):
        print (f"COURSE REQUEST: ACTION {task}")
        print (f"Process by {searchBy}")
        print ('Request:\n ')
        print (request)
        payload={}
        if (request.GET.get('isAvailabilityUpdateRequired1')):
            if (request.GET.get('isAvailabilityUpdateRequired1') == 'true'):
                payload={'availability':{"available":request.GET.get('selectedAvailability')}}
        if (request.GET.get('isDataSourceKeyUpdateRequired1')):
            if (request.GET.get('isDataSourceKeyUpdateRequired1') == 'true'):
                payload["dataSourceId"] = request.GET.get('selectedDataSourceKey')
            
        print ("PAYLOAD\n")
        for x, y in payload.items():
            print(x, y)

        # Build and make bb request...
        if (searchBy == 'externalId'):
            crs="externalId:" + searchValue
        elif (searchBy == 'primaryId'):
            crs=searchValue
            print(f"course pattern: {crs}")
        elif (searchBy == 'courseId'):
            crs="courseId:" + searchValue
            print(f"course pattern: {crs}")

        print(f"course pattern: {crs}")

        resp = bb.UpdateCourse(courseId = crs, payload=payload, params = {'fields':'id, courseId, externalId, name, availability.available, dataSourceId, created'}, sync=True )
        if (resp.status_code == 200):
            result_json = resp.json() #return actual error
            dskresp = bb.GetDataSource(dataSourceId = result_json['dataSourceId'], sync=True)
            dsk_json = dskresp.json()
            result_json['dataSourceId'] = dsk_json['externalId']

            context = {
              'result_json': result_json,
            }
        else:
            error_json = resp.json()
            print (f"RESPONSE:\n", error_json)
            context = {
                'error_json': error_json,
            }

        return render(request, 'courses.html', context=context)

    return render(request, 'courses.html')

def users(request):
    task = request.GET.get('task')
    searchBy = request.GET.get('searchBy')
    searchValueUsr = request.GET.get('searchValueUsr')
    print ("SEARCHBY: ", searchBy)
    print ("SEARCHVALUEUSR: ", searchValueUsr)
    print ("TASK: ", task)

    """View function for users page of site."""
    bb_json = request.session.get('bb_json')
    if (bb_json is None):
        bb = BbRest(KEY, SECRET, f"https://{LEARNFQDN}" )
        bb_json = jsonpickle.encode(bb)
        print('pickled BbRest putting it on session')
        request.session['bb_json'] = bb_json
        request.session['target_view'] = 'courses'
        return HttpResponseRedirect(reverse('get_auth_code'))
    else:
        print('got BbRest from session')
        bb = jsonpickle.decode(bb_json)
        if bb.is_expired():
            print('expired token')
            request.session['bb_json'] = None
            whoami(request)
        bb.supported_functions() # This and the following are required after
        bb.method_generator()    # unpickling the pickled object.
        print(f'expiration: {bb.expiration()}')
    
    if (task == 'search'):
        #Process request...
        print (f"USERS REQUEST: ACTION {task}")
        searchValueUsr = request.GET.get('searchValue')
        print (f"USERS REQUEST: USR: {searchValueUsr}")
        print (f"Process by {searchBy}")
        if (searchBy == 'externalId'):
            usr="externalId:" + searchValueUsr
            print(f"user pattern: {usr}")
        elif (searchBy == 'userName'):
            usr="userName:" + searchValueUsr
            print(f"user pattern: {usr}")
        resp = bb.GetUser(userId = usr, params = {'fields':'id, userName, name.given, name.middle, name.family, externalId, contact.email, availability.available, dataSourceId, created'}, sync=True )
        if (resp.status_code == 200):
            user_json = resp.json() 
            dskresp = bb.GetDataSource(dataSourceId = user_json['dataSourceId'], sync=True)
            dsk_json = dskresp.json()
            user_json['dataSourceId'] = dsk_json['externalId']
            user_json['searchValueUsr'] = searchValueUsr
            user_json['searchBy'] = searchBy
            dskresp = bb.GetDataSources(params={'fields':'id, externalId'}, sync=True)
            dsks_json = dskresp.json()
            print ("DSKS:\n", dsks_json["results"])
            dsks = dsks_json["results"]
            dsks = sortDsk(dsks)
            print ("SIZE OF DSK LIST:", len(dsks))
                
            context = {
              'user_json': user_json,
              'dsks_json': dsks,
            }
        else:
            error_json = resp.json()
            print (f"RESPONSE:\n", error_json)
            context = {
                'error_json': error_json,
            }

        return render(request, 'users.html', context=context)

    if (task == 'process'):
        print (f"USERS REQUEST: ACTION {task}")
        print (f"Process by {searchBy}")
        print ('Request:\n ')
        print (request)
        payload={}
        if (request.GET.get('isAvailabilityUpdateRequired1')):
            if (request.GET.get('isAvailabilityUpdateRequired1') == 'true'):
                payload={'availability':{"available":request.GET.get('selectedAvailability')}}
        if (request.GET.get('isDataSourceKeyUpdateRequired1')):
            if (request.GET.get('isDataSourceKeyUpdateRequired1') == 'true'):
                payload["dataSourceId"] = request.GET.get('selectedDataSourceKey')
            
        print ("PAYLOAD\n")
        for x, y in payload.items():
            print(x, y)

        # Build and make bb request...
        if (searchBy == 'externalId'):
            usr="externalId:" + searchValueUsr
        elif (searchBy == 'userName'):
            usr="userName:" + searchValueUsr

        print(f"user pattern: {usr}")

        resp = bb.UpdateUser(userId = usr, payload=payload, params = {'fields':'id, userName, name.given, name.middle, name.family, externalId, contact.email, availability.available, dataSourceId, created'}, sync=True )
        if (resp.status_code == 200):
            result_json = resp.json() #return actual error
            dskresp = bb.GetDataSource(dataSourceId = result_json['dataSourceId'], sync=True)
            dsk_json = dskresp.json()
            result_json['dataSourceId'] = dsk_json['externalId']

            context = {
              'result_json': result_json,
            }
        else:
            error_json = resp.json()
            print (f"RESPONSE:\n", error_json)
            context = {
                'error_json': error_json,
            }

        return render(request, 'users.html', context=context)

    return render(request, 'users.html')


def enrollments(request):
    task = request.GET.get('task')
    searchBy = request.GET.get('searchBy')

    bb_json = request.session.get('bb_json')
    if (bb_json is None):
        bb = BbRest(KEY, SECRET, f"https://{LEARNFQDN}" )
        bb_json = jsonpickle.encode(bb)
        print('pickled BbRest putting it on session')
        request.session['bb_json'] = bb_json
        request.session['target_view'] = 'whoami' 
        return HttpResponseRedirect(reverse('get_auth_code'))
    else:
        print('got BbRest from session')
        bb = jsonpickle.decode(bb_json)
        if bb.is_expired():
            print('expired token')
            request.session['bb_json'] = None
            whoami(request)
        bb.supported_functions() # This and the following are required after
        bb.method_generator()    # unpickling the pickled object.
        print(f'expiration: {bb.expiration()}')
    
    if (task == 'search'):
        #Process request...
        print (f"ENROLLMENTS REQUEST: ACTION {task}")
        searchValueCrs = request.GET.get('searchValueCrs')
        searchValueUsr = request.GET.get('searchValueUsr')
        print (f"ENROLLMENTS REQUEST: CRS: {searchValueCrs}")
        print (f"ENROLLMENTS REQUEST: USR: {searchValueUsr}")

        if (searchBy == 'byCrsUsr'):
            print ("Process by Course AND User")
            crs="externalId:" + searchValueCrs
            usr="externalId:" + searchValueUsr
            resp = bb.GetMembership(courseId=crs, userId = usr, params = {'expand':'user', 'fields':'id, user.userName, user.name.given, user.name.middle, user.name.family, user.externalId, user.contact.email, availability.available, user.availability.available, dataSourceId, created'}, sync=True )
            if (resp.status_code == 200):
                member_json = resp.json() 
                dskresp = bb.GetDataSource(dataSourceId = member_json['dataSourceId'], sync=True)
                dsk_json = dskresp.json()
                member_json['dataSourceId'] = dsk_json['externalId']
                member_json['crsExternalId'] = searchValueCrs
                member_json['usrExternalId'] = searchValueUsr
                member_json['searchBy'] = searchBy
                dskresp = bb.GetDataSources(params={'fields':'id, externalId'}, sync=True)
                dsks_json = dskresp.json()
                print ("DSKS:\n", dsks_json["results"])
                dsks = dsks_json["results"]
                dsks = sortDsk(dsks)
                print ("SIZE OF DSK LIST:", len(dsks))
                
                context = {
                  'member_json': member_json,
                  'dsks_json': dsks,
                }
            else:
                error_json = resp.json()
                print (f"RESPONSE:\n", error_json)
                context = {
                    'error_json': error_json,
                }

            return render(request, 'enrollments.html', context=context)

        elif (searchBy == 'byCrs'):
            print ("Process by Course Only")
            error_json = {
                'message': 'Searching by Course is not currently supported'
            }
            print (f"RESPONSE:\n", error_json)
            context = {
                'error_json': error_json,
            }
            return render(request, 'enrollments.html', context=context)

        elif (searchBy == 'byUsr'):
            print ("Process by User Only")
            error_json = {
                'message': 'Searching by Course is not currently supported'
            }
            print (f"RESPONSE:\n", error_json)
            context = {
                'error_json': error_json,
            }
            return render(request, 'enrollments.html', context=context)

        else: 
            print ("Cannot process request")
            error_json = {
                'message': 'Cannot process request'
            }
            print (f"RESPONSE:\n", error_json)
            context = {
                'error_json': error_json,
            }
            return render(request, 'enrollments.html', context=context)


    elif (task == 'process'):
        # print incoming parameters and then afterward submit the patch request.
        
        if (searchBy == 'byCrsUsr'):
            print ("processing by crsusr")
            print ('Request:\n ')
            print (request)

            payload={}
            if (request.GET.get('isAvailabilityUpdateRequired1')):
                if (request.GET.get('isAvailabilityUpdateRequired1') == 'true'):
                    payload={'availability':{"available":request.GET.get('selectedAvailability')}}
            if (request.GET.get('isDataSourceKeyUpdateRequired1')):
                if (request.GET.get('isDataSourceKeyUpdateRequired1') == 'true'):
                    payload["dataSourceId"] = request.GET.get('selectedDataSourceKey')
            
            print ("PAYLOAD\n")
            for x, y in payload.items():
                print(x, y)

            # Build and make bb request...
            crs = "externalId:"+request.GET.get('crsExternalId')
            print ("crs:", crs)
            usr = "externalId:"+request.GET.get('usrExternalId')
            print ("usr", usr)

            resp = bb.UpdateMembership(courseId=crs, userId = usr, payload=payload, params = {'expand':'user', 'fields':'id, user.userName, user.name.given, user.name.middle, user.name.family, user.externalId, user.contact.email, availability.available, user.availability.available, dataSourceId, created'}, sync=True )
            if (resp.status_code == 200):
                result_json = resp.json() #return actual error
                dskresp = bb.GetDataSource(dataSourceId = result_json['dataSourceId'], sync=True)
                dsk_json = dskresp.json()
                result_json['dataSourceId'] = dsk_json['externalId']

                context = {
                  'result_json': result_json,
                }
            else:
                error_json = resp.json()
                print (f"RESPONSE:\n", error_json)
                context = {
                    'error_json': error_json,
                }

            return render(request, 'enrollments.html', context=context)


            # crs="externalId:" + searchValueCrs
            # usr="externalId:" + searchValueUsr
            # resp = bb.UpdateMembership(courseId=crs, userId = usr, params = {'expand':'user', 'fields':'id, user.userName, user.name.given, user.name.middle, user.name.family, user.externalId, user.contact.email, availability.available, user.availability.available, dataSourceId, created'}, sync=True )
            # if (resp.status_code == 200):
            #     member_json = resp.json() #return actual error
            #     dskresp = bb.GetDataSource(dataSourceId = member_json['dataSourceId'], sync=True)
            #     dsk_json = dskresp.json()
            #     member_json['dataSourceId'] = dsk_json['externalId']
            #     member_json['crsExternalId'] = searchValueCrs
            #     member_json['searchBy'] = searchBy
            #     dskresp = bb.GetDataSources(params={'fields':'id, externalId'}, sync=True)
            #     dsks_json = dskresp.json()
            #     print ("DSKS:\n", dsks_json["results"])
            #     print ("SIZE OF DSK LIST:", len(dsks_json["results"]))
                
            #     context = {
            #       'member_json': member_json,
            #       'dsks_json': dsks_json["results"],
            #     }
            # else:
            #     error_json = resp.json()
            #     print (f"RESPONSE:\n", error_json)
            #     context = {
            #         'error_json': error_json,
            #     }

            #return render(request, 'enrollments.html', context=context)

        result_json = {"brand": "Ford", "model": "Mustang", "year": 1964 }

        print (f"RESPONSE:\n", result_json)

        context = {     
            'result_json': result_json,
        }

        return render(request, 'enrollments.html', context=context)

    else:
        return render(request, 'enrollments.html')

def get_auth_code(request):
    # Happens when the user hits whoami the first time and hasn't authenticated on Learn
    # Part I. Request an authroization code oauth2/authorizationcode
    print(f"In get_auth_code: REQUEST URI:{request.build_absolute_uri()}")
    bb_json = request.session.get('bb_json')
    print('got BbRest from session')
    bb = jsonpickle.decode(bb_json)
    bb.supported_functions() # This and the following are required after
    bb.method_generator()    # unpickling the pickled object. 
    # The following gives the path to the resource on the server where we are running, 
    # but not the protocol or host FQDN. We need to prepend those to get an absolute redirect uri.
    redirect_uri = reverse(get_access_token)
    absolute_redirect_uri = f"https://{request.get_host()}{redirect_uri}"
    # absolute_redirect_uri = request.build_absolute_uri(redirect_uri)
    authcodeurl = bb.get_auth_url(redirect_uri=absolute_redirect_uri)

    print(f"AUTHCODEURL:{authcodeurl}")
    return HttpResponseRedirect(authcodeurl)

def get_access_token(request):
    # Happens when the user hits whoami the first time and hasn't authenticated on Learn
    # Part II. Get an access token for the user that logged in. Put that on their session.
    bb_json = request.session.get('bb_json')
    target_view = request.session.get('target_view')
    print('got BbRest from session')
    bb = jsonpickle.decode(bb_json)
    bb.supported_functions() # This and the following are required after
    bb.method_generator()    # unpickling the pickled object.
    # Next, get the code parameter value from the request
    redirect_uri = reverse(get_access_token)
    absolute_redirect_uri = f"https://{request.get_host()}{redirect_uri}"
    code =  request.GET.get('code', default = None)
    if (code == None):
        exit()
    #Rebuild a new BbRest object to get an access token with the user's authcode.
    user_bb = BbRest(KEY, SECRET, f"https://{LEARNFQDN}", code=code, redirect_uri=absolute_redirect_uri )
    bb_json = jsonpickle.encode(user_bb)
    print('pickled BbRest putting it on session')
    request.session['bb_json'] = bb_json
    return HttpResponseRedirect(reverse(f'{target_view}'))

def getusers(request):
    """View function for getusers page of site."""
    bb_json = request.session.get('bb_json')
    if (bb_json is None):
        bb = BbRest(KEY, SECRET, f"https://{LEARNFQDN}" )
        bb_json = jsonpickle.encode(bb)
        print('pickled BbRest putting it on session')
        request.session['bb_json'] = bb_json
        request.session['target_view'] = 'getusers'
        return HttpResponseRedirect(reverse('get_auth_code'))
    else:
        print('got BbRest from session')
        bb = jsonpickle.decode(bb_json)
        if bb.is_expired():
            print('expired token')
            request.session['bb_json'] = None
            whoami(request)
        bb.supported_functions() # This and the following are required after
        bb.method_generator()    # unpickling the pickled object.
        print(f'expiration: {bb.expiration()}')

    resp = bb.GetUsers()
    user_json = resp.json()
    context = {
        'user_json': user_json,
    }
    print('views.py index(request) calling render...')
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'getusers.html', context=context)

def sortDsk(dsks):
  return sorted(dsks, key=lambda x: x['externalId'])

def learnlogout(request):
    request.session.flush()
    return HttpResponseRedirect(f"https://{LEARNFQDN}/webapps/login?action=logout")

import json
from django.urls import reverse
from django.shortcuts import render, redirect
from googleapiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from google.oauth2.credentials import Credentials
from django.contrib.auth import logout
import requests
import datetime # To generate timestamps

SCOPES = [
    'https://www.googleapis.com/auth/drive.metadata.readonly', 
    'https://www.googleapis.com/auth/userinfo.email', 
    'https://www.googleapis.com/auth/userinfo.profile', 
    'openid'
    ]

REDIRECT_URI = 'http://127.0.0.1:8000/auth/'

# Create a OAuth 2.0 authorization flow using the client secrets 
# file ('credentials.json') downloaded from the Google API Console.
flow = Flow.from_client_secrets_file(
    'credentials.json',
    scopes = SCOPES,
    redirect_uri = REDIRECT_URI)


# @require_auth decorator
def require_auth(function):
    def wrapper(request, *args, **kwargs):
        user = request.session.get('user')
        access_token = request.session.get('token')

        # If there is an active user session (i.e. a user is logged in)
        if user and access_token:
            # Creates a Credentials (google.auth.credentials.Credentials) 
            # instance from parsed authorized user info stored in the 
            # session key 'token'.
            # This Credentials object is required (as a parameter) for 
            # authentication by the Google API call request resource 
            # builder (googleapiclient.discovery.build).
            creds = Credentials.from_authorized_user_info(access_token)

            # Validate user's credentials (access token)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                    # Store refreshed access token in session
                    request.session['token'] = json.loads(creds.to_json())
                    # return the wrapped function
                    return function(request, *args, **kwargs)
                else:
                    # If in doubt, just logout to clear session and cookies.
                    logout(request)
                    return redirect('/login')
            else:
                return function(request, *args, **kwargs)
        else:
            logout(request)
            return redirect('/login')
    return wrapper


@require_auth
def home(request):
    # Retrieve User Info and access token, if any, from session
    user = request.session.get('user')
    access_token = request.session.get('token')
    messages = request.session.get('messages', {})

    ## 1. Using Google API Client library ##

    creds = creds = Credentials.from_authorized_user_info(access_token)
    api_call_return = {}

    # Construct a Resource to interact with the Drive API
    service = build('drive', 'v3', credentials=creds)

    try:
        # Make the API request.
        response = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()

        if 'error' in response:
            # The API executed, but Drive service returned an error.
            api_call_error = response['error']['details'][0]
            messages.setdefault('errors', []).append({'usr_msg': 'API Call error.', 'sys_msg': str(api_call_error['errorMessage'])})

        else:
            api_call_return = response['files']

    except errors.HttpError as e:
        # The API encountered a problem before reaching Google Drive
        messages.setdefault('errors', []).append({'usr_msg': 'HTTP request error.', 'sys_msg': e.content})

    ## 2. Using plain HTTP requests with bearer authentication ##

    bearer_auth_token = access_token['token']
    hreq_bearer_auth_api_call_return = {}
    hreq_url = 'https://www.googleapis.com/drive/v3/files?alt=json' # API endpoint
    hreq_headers = {
        'Authorization': 'Bearer ' + bearer_auth_token,
        'Content-Type': 'application/json'
        }
    folder_name = datetime.datetime.now().strftime("[%Y-%m-%d %H-%M-%S] Auto-created")
    hreq_payload = {
        'mimeType':'application/vnd.google-apps.folder',
        'name':folder_name
        }

    try:
        hreq_bearer_auth_api_call_return = requests.post(hreq_url, headers=hreq_headers, json=hreq_payload)
        hreq_bearer_auth_api_call_return.raise_for_status()
        hreq_bearer_auth_api_call_return = hreq_bearer_auth_api_call_return.json()

    except requests.exceptions.RequestException as e:
        messages.setdefault('errors', []).append({'usr_msg': 'API Call (plain HTTP request with bearer authentication) error.', 'sys_msg': e})

    # Store all messages into session; to be added to template's context object
    request.session['messages'] = messages
    session_messages = request.session.pop('messages', None)

    return render(request, 'home.html', context={'user': user, 'messages': session_messages, 'api_call_return': api_call_return, 'hreq_bearer_auth_api_call_return': hreq_bearer_auth_api_call_return})


def login(request):
    user = request.session.get('user')

    if user :
        # If user is already logged in, redirect to home page.
        messages = request.session.get('messages', {})
        messages.setdefault('warning', []).append({'usr_msg': 'User already logged in. Redirected to home page.', 'sys_msg': ''})
        request.session['messages'] = messages
        return redirect('/')
    else:
        # Get the authorization URL and redirect to it.
        auth_url, _ = flow.authorization_url(prompt='consent')
        return redirect(auth_url)


def auth(request):
    messages = request.session.get('messages', {})

    try:
        # Get the authorization code, that is provided as a 
        # GET parameter passed to the redirect URI,
        # after consent is granted by the user.
        code = request.GET.get('code','')

        # Use the authorization code to get (fetch) the access token.
        flow.fetch_token(code=code)

        # Create a JSON string representation of the Credentials 
        # object containing (among other items) the access token 
        # that has just been fetched.
        json_creds = flow.credentials.to_json()

        # Convert the JSON representation of the Credentials object
        # to a Python dictionary, in order to store it as a session key.
        dict_creds = json.loads(json_creds)

    # If the '/auth' URL is not requested (with valid parameters)
    # in a OAuth2 authentication flow, redirect to home page
    except Exception as e:
        messages.setdefault('errors', []).append({'usr_msg': 'Error occured. Redirected to home page.', 'sys_msg': str(e)})
        request.session['messages'] = messages

        return redirect('/')

    # Store the decoded JSON string representation of the Credentials 
    # object as a session key named 'token'. This dictionary contains 
    # (among other items): the access token, its expiry datetime, and the refresh token.
    request.session['token'] = dict_creds

    # Retrieve (and store as a session key named 'user') user information, by parsing 
    # the Open ID Connect ID Token contained in the Credentials object.
    # This session key uniquely identifies a logged in user.
    request.session['user'] = id_token.verify_oauth2_token(flow.credentials.id_token, Request())

    messages.setdefault('info', []).append({'usr_msg': 'User successfully logged in.', 'sys_msg': ''})
    request.session['messages'] = messages

    return redirect('/')


# logout view: clears cookies from the browser 
# and the corresponding session from Django's DB
def logout_view(request):
    logout(request)
    return redirect('/')

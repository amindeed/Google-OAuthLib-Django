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

SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', 'openid']
REDIRECT_URI = 'http://127.0.0.1:8000/auth/'

flow = Flow.from_client_secrets_file(
    'credentials.json',
    scopes = SCOPES,
    redirect_uri = REDIRECT_URI)


def home(request):
    user = request.session.get('user')
    access_token = request.session.get('token')
    messages = request.session.get('messages', {})
    creds = None
    api_call_return_value = {}

    if user:
        
        if access_token:
            creds = Credentials.from_authorized_user_info(access_token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                request.session['token'] = json.loads(creds.to_json())
            else:
                logout(request)
                return render(request, 'home.html')

        service = build('drive', 'v3', credentials=creds)

        try:
            response = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()

            if 'error' in response:
                api_call_error = response['error']['details'][0]
                messages.setdefault('errors', []).append({'usr_msg': 'API Call error.', 'sys_msg': str(api_call_error['errorMessage'])})

            else:
                api_call_return_value = response['files']

        except errors.HttpError as e:
            messages.setdefault('errors', []).append({'usr_msg': 'API Call error.', 'sys_msg': e.content})
    
    request.session['messages'] = messages
    session_messages = request.session.pop('messages', None)

    return render(request, 'home.html', context={'user': user, 'messages': session_messages, 'api_call_return_value': api_call_return_value})


def login(request):
    user = request.session.get('user')

    if user :
        messages = request.session.get('messages', {})
        messages.setdefault('warning', []).append({'usr_msg': 'User already logged in. Redirected to home page.', 'sys_msg': ''})
        request.session['messages'] = messages
        return redirect('/')
    else:
        auth_url, _ = flow.authorization_url(prompt='consent')
        return redirect(auth_url)


def auth(request):
    messages = request.session.get('messages', {})

    try:
        code = request.GET.get('code','')
        flow.fetch_token(code=code)

        json_creds = flow.credentials.to_json()
        dict_creds = json.loads(json_creds)

    except Exception as e:
        messages.setdefault('errors', []).append({'usr_msg': 'Error occured. Redirected to home page.', 'sys_msg': str(e)})
        request.session['messages'] = messages

        return redirect('/')

    request.session['token'] = dict_creds
    request.session['user'] = id_token.verify_oauth2_token(flow.credentials.id_token, Request())
    messages.setdefault('info', []).append({'usr_msg': 'User successfully logged in.', 'sys_msg': ''})
    request.session['messages'] = messages

    return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('/')

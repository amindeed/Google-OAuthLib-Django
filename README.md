# Google OAuthLib Django

[![Lines of code](https://img.shields.io/tokei/lines/github/amindeed/Google-OAuthLib-Django?logo=visual-studio-code)](/google_oauthlib_quickstart)
[![Python](https://img.shields.io/badge/Python-v3.9.1-yellowgreen?logo=python&logoColor=ffffff)](https://www.python.org/downloads/release/python-391/)
[![Django](https://img.shields.io/badge/Django-v3.1.8-green?logo=django)](https://docs.djangoproject.com/en/3.1/releases/3.1.8/)
[![Google API Python Client](https://img.shields.io/badge/API%20Client-v1.12.8-blue?logo=google&logoColor=81CAFA)](https://pypi.org/project/google-api-python-client/1.12.8/)
[![Google Auth OAuthLib](https://img.shields.io/badge/Google%20Auth%20OAuthLib-v0.4.2-blue?logo=google&logoColor=81CAFA)](https://pypi.org/project/google-auth-oauthlib/0.4.2/)
[![License](https://img.shields.io/github/license/amindeed/Google-OAuthLib-Django?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABIAAAAYCAYAAAD3Va0xAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAABYlAAAWJQFJUiTwAAAAB3RJTUUH5QMcESAcS1MDzAAAAj1JREFUOMuVlDtoVFEQhr+zu0pik0C6YLQwIDaJjRY2aSyNj9ikkaC1QhAjFkI0YhWrgCJ2SnwgiqAiNhaiVnY+IqTQ+AoWSrLiIyZmPwvnLtc12dWBwz13Zs7MPzP/OYkQNdsWgFWx7wDGgATsB96F/htQSSmRP1SVMFwDnsWaAGaAT8CL0D0FzqeU8slJ2U8YdgI3gBFA4AnwCqgAnUAXsACcALamlO6p5JGh7lC/qhfUfvW5v2VGnY39hLpHPad+UbdX26KiXg/Hy+qB2I+rzblETZFEdUi9GvtbmUOz+lo9pvaFcXd+CPleqL3hs00dVstqIQs0pR5RJ9VxlpEsYJT2Mc7MZIHWRYZ98W2hgagd4Tsc366sP3fVjepsDafqoVpUe9RH6pUC0A5MAStjtP8qi0AJeAm0o3YHvH7rQfkTVWtueqo9BWASeANsAKbVk8uVl9MdBD4DLcAs8LAQDBb4EPdqSF1fewUyBqurgaPAcWA6zBXUknpH/a7uVS+pc+qA2lpTzoD6M4g7EOy+n89WDMOiOqYORu1z6nSsudAdVkfVSiQuEc9DHvYgMAr0Ak1AT0wnAUXgAVAGbgKHUkpn/rq0OXTZZZ1Xf6hn1dOBaCFsjxuNNUO4Kco8pb5V36sjUU5n3rcRa7sj+1q1JVZbBFqzFD2WeiGrvQOKKaVySqkcParaavtSakDiiloAVgTXlpVCHVsCtgDzManN9QLVQ1QELgYdEnCb/5V4o+bVvpxuV7C6bakzvwBluHvhBl+OCQAAAABJRU5ErkJggg==)](/LICENSE)


<p align="center">
  <img src="/logos.png" alt="Google APIs + OAuth2 + OIDC + Django"/>
</p>


**Google OAuthLib Django** is a Django boilerplate app implementing a full Google OAuth2 authentication flow using [`google-auth-oauthlib`](https://github.com/googleapis/google-auth-library-python-oauthlib) with [Sessions](https://docs.djangoproject.com/en/3.1/topics/http/sessions/#using-sessions-in-views).

This is not intended as a replacement for Django's users sign up/in mechanism. [Django AllAuth](https://github.com/pennersr/django-allauth) is more suited for such use case. 

The App uses basic [Django Sessions](https://docs.djangoproject.com/en/3.1/topics/http/sessions/#using-sessions-in-views) to let users make authenticated requests that target their Google accounts resources. No user data is kept after logout.

## Table of Contents

- [Features](#features)
- [Compatibility](#compatibility)
- [Setup](#setup)
  - [Install and configure requirements](#install-and-configure-requirements)
  - [Option 1: Cloning and running the code from this repository](#option-1-cloning-and-running-the-code-from-this-repository)
  - [Option 2: Update an existing Django project/app](#option-2-update-an-existing-django-projectapp)
    - _[Add files](#-add-files)_
    - _[Modify files](#-modify-files)_
- [Background](#background)
  - [About AuthLib](#about-authlib)
  - [Google AppsScript/Drive API Python Quickstart code adaptation](#google-appsscriptdrive-api-python-quickstart-code-adaptation)
  - [Online Resources](#online-resources)
- [License](#license)


<p align="center">
  <img src="/google-oauthlib-django.gif" alt="google-oauthlib-django.gif" width="500"/>
</p>


## Features

- Full OAuth2 authentication flow, with automatic access token refresh.
- Supporting two mechanisms:
    - Using a Google service API client library, [via](https://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.discovery-module.html#build) the Google API [Discovery](https://developers.google.com/discovery) resource constructor (`googleapiclient.discovery.build`).
    - Sending plain HTTP requests to a Google service API's endpoint, using a Bearer authentication scheme.
- Identifying users by parsing OIDC tokens.
- Handling backend errors, warnings and infos, and storing their respective messages to the session key `messages`, which is added as a variable to template's context, and then rendered on the frontend.
- Handling access to some special paths like `/login` and `/auth`.
- `@require_auth` decorator for views.
- logout view function, that clears browser cookies along with the corresponding session from Django's database.

## Compatibility

The code was tested in the following environments (all OSs are x64):

|                                | Windows 10                   | CentOS 7 | CentOS 8 Stream | Ubuntu 16.04 | Ubuntu 18.04 | Ubuntu 20.04 |
|--------------------------------|------------------------------|----------|-----------------|--------------|--------------|--------------|
| **`Python`**                   | `3.9.1`                      |    -     |       -         |      -       |      -       |      -       |
| **`Django`**                   | ***`3.2`*** - <br>`3.1.8`    |    -     |       -         |      -       |      -       |      -       |
| **`Google API Python Client`** | ***`2.1.0`*** - <br>`1.12.8` |    -     |       -         |      -       |      -       |      -       |
| **`Google Auth OAuthLib`**     | ***`0.4.4`*** - <br>`0.4.2`  |    -     |       -         |      -       |      -       |      -       |

## Setup
### Install and configure requirements

- Create a GCP project, enable Drive API, add the following scopes and then download webapp Client ID credentials file from the GCP console:

    ```
    https://www.googleapis.com/auth/drive
    https://www.googleapis.com/auth/userinfo.email
    https://www.googleapis.com/auth/userinfo.profile
    openid
    ```

- Create a virtual environment and install required libraries:

    ```bash
    virtualenv venv
    source venv/Scripts/activate
    pip install Django google-api-python-client google-auth-oauthlib
    ## OR: 'pip install -r requirements.txt'
    ```

### Option 1: Cloning and running the code from this repository

Clone the repository, create the Django database and launch the dev server:

```bash
git clone git@github.com:amindeed/Google-OAuthLib-Django.git
cd Google-OAuthLib-Django
# Migrate changes to Django's DB (only in first time run)
python manage.py migrate
python manage.py runserver
```

### Option 2: Update an existing Django project/app

Diffing changes between the code in this repository and a newly created Django project (`django-admin startproject my_django_app .`):

#### ➕ Add files:

- **`credentials.json`** (GCP project Client ID credentials)
- **`my_django_app/templates/home.html`** ( [`templates/home.html`](/google_oauthlib_quickstart/templates/home.html) sample base template)
- **`my_django_app/views.py`** ([`views.py`](/google_oauthlib_quickstart/views.py))
- **`db.sqlite3`** (automatically created by Django by running `python manage.py migrate`)

#### ✎ Modify files:

- Modify **`my_django_app/settings.py`**: Django admin site and static files apps are disabled. For middleware, only `SessionMiddleware` is kept, which is enough for the intended use case.

    ```diff
    @@ -8,7 +8,7 @@ BASE_DIR = Path(__file__).resolve().parent.parent
    # See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    -SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    +SECRET_KEY = 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    @@ -19,12 +19,12 @@ ALLOWED_HOSTS = []
    # Application definition

    INSTALLED_APPS = [
    -    'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
    -    'django.contrib.staticfiles',
    +
    +    'my_django_app',
    ]

    MIDDLEWARE = [
    @@ -32,8 +32,6 @@ MIDDLEWARE = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
    -    'django.contrib.auth.middleware.AuthenticationMiddleware',
    -    'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    ```

- Modify **`my_django_app/urls.py`**: All lines of code related to the Django admin site are removed.

    ```diff
    -from django.contrib import admin
    from django.urls import path
    +from my_django_app import views

    urlpatterns = [
    -    path('admin/', admin.site.urls),
    +    path('', views.home),
    +    path('login/', views.login),
    +    path('auth/', views.auth, name='auth'),
    +    path('logout/', views.logout_view),
    ]
    ```


## Background

_The code in this repository was a result of my researches for another project: [`GMail-AutoResponder`](https://github.com/amindeed/Gmail-AutoResponder/blob/master/worklog.md#2021-02-15-code)_.

The structure of the code was built upon the [AuthLib library demo for Django](https://github.com/authlib/demo-oauth-client/tree/310c6f1da26abc32f8eca8668d1b6d0aa4a9f0a3/django-google-login) and the [Google Apps Script API Python Quickstart](https://github.com/googleworkspace/python-samples/tree/aacc00657392a7119808b989167130b664be5c27/apps_script/quickstart) (and later, the [Drive V3 Python Quickstart](https://github.com/googleworkspace/python-samples/tree/master/drive/quickstart), for simpler API calls):

### About AuthLib

**[AuthLib](https://github.com/lepture/authlib)** would have been my goto library, but I dropped it after many tries, due to confusing instructions about OAuth2 refresh token support for Django _(at least, up until February 2021)_:

- _[python - Getting refresh_token with lepture/authlib - Stack Overflow](https://stackoverflow.com/questions/48907773/getting-refresh-token-with-lepture-authlib)_
    - > _`client_credentials` won't issue refresh token. You need to use authorization_code flow to get the refresh token._
        - _A OAuth server-side configuration seems to be needed: [stackoverflow.com/questions/51305430/…](https://stackoverflow.com/questions/51305430/obtaining-refresh-token-from-lepture-authlib-through-authorization-code/51305975#51305975)_
- _[Refresh and Auto Update Token · Issue #245 · lepture/authlib](https://github.com/lepture/authlib/issues/245)_
    - > _Also be aware, unless you're on authlib 0.14.3 or later, the django integration is broken for refresh (If you're using the metadata url): [RemoteApp.request fails to use token_endpoint to refresh the access token · Issue #193 · lepture/authlib](https://github.com/lepture/authlib/issues/193)_

### Google AppsScript/Drive API Python Quickstart code adaptation:

- `credentials.json` contains [OAuth client ID credentials](https://developers.google.com/identity/protocols/oauth2/web-server#creatingcred) of the GCP project, that will provide access to Google user's resources for the Django app.
- [`Flow`](https://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html#google_auth_oauthlib.flow.Flow) class was used instead of [`InstalledAppFlow`](https://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html#google_auth_oauthlib.flow.InstalledAppFlow).
- Instead of [pickles](https://github.com/googleworkspace/python-samples/blob/aacc00657392a7119808b989167130b664be5c27/apps_script/quickstart/quickstart.py#L65), [JSON Serialization](#tojson) of Credentials is used: OAuth2 token (a [`Credentials`](https://google-auth.readthedocs.io/en/stable/reference/google.oauth2.credentials.html#google.oauth2.credentials.Credentials) instance) is converted to a dictionary and saved to the session (as a session key named `token`):

    ```
    {
        'token': 'XXXXXXXXX',
        'refresh_token': 'YYYYYYY',
        'token_uri': 'https://oauth2.googleapis.com/token',
        'client_id': 'a0a0a0a0a0a0a0a0a0.apps.googleusercontent.com',
        'client_secret': 'ZZZZZZZZZ',
        'scopes': [
            'https://www.googleapis.com/auth/drive.metadata.readonly', 
            'https://www.googleapis.com/auth/userinfo.email', 
            'https://www.googleapis.com/auth/userinfo.profile', 
            'openid'
            ],
        'expiry': '2021-03-06T12:34:52.214490Z'
    }
    ```

- Value of the session key `user` (which identifies the logged in user) is retrieved by [parsing](https://google-auth.readthedocs.io/en/stable/reference/google.oauth2.id_token.html#google.oauth2.id_token.verify_oauth2_token) the [Open ID Connect ID Token](https://google-auth.readthedocs.io/en/stable/reference/google.oauth2.credentials.html#google.oauth2.credentials.Credentials.id_token) contained in the Credentials object resulting from a complete and successful OAuth2 flow.

    ```
    {
        'iss': 'https://accounts.google.com',
        'azp': 'xxxxxxxxxxx.apps.googleusercontent.com',
        'aud': 'yyyyyyyyyyy.apps.googleusercontent.com',
        'sub': '0000000000000000000',
        'hd': 'mydomain.com',
        'email': 'user@mydomain.com',
        'email_verified': True,
        'at_hash': 'ZZZZZZZZZZZZZ',
        'name': 'Awesome User',
        'picture': 'https://xy0.googleusercontent.com/aa/bb/photo.jpg',
        'given_name': 'Awesome',
        'family_name': 'User',
        'locale': 'en',
        'iat': 111111111,
        'exp': 222222222
    }
    ```

### Online Resources:

- [`Flow.fetch_token(code=code)`](https://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html#google_auth_oauthlib.flow.Flow.fetch_token) method of the [`google_auth_oauthlib.flow.Flow` class](https://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html) (`google-auth-oauthlib 0.4.1` documentation).
- [`Flow.credentials`](https://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html#google_auth_oauthlib.flow.Flow.credentials) constructs a [`google.oauth2.credentials.Credentials`](https://google-auth.readthedocs.io/en/stable/reference/google.oauth2.credentials.html#google.oauth2.credentials.Credentials) class, which in turn is a child class of [`google.auth.credentials.Credentials`](https://google-auth.readthedocs.io/en/stable/reference/google.auth.credentials.html#google.auth.credentials.Credentials)
- Key [`google.auth.credentials.Credentials`](https://google-auth.readthedocs.io/en/stable/reference/google.auth.credentials.html#google.auth.credentials.Credentials) members, that are inherited by the [`google_auth_oauthlib.flow.Flow.credentials`](https://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html#google_auth_oauthlib.flow.Flow.credentials) class:
    - <a name="tojson"></a>[`to_json()`](https://google-auth.readthedocs.io/en/stable/reference/google.oauth2.credentials.html#google.oauth2.credentials.Credentials.to_json): Returns A JSON representation of this instance. When converted into a dictionary, it can be passed to [`from_authorized_user_info()`](https://google-auth.readthedocs.io/en/stable/reference/google.oauth2.credentials.html#google.oauth2.credentials.Credentials.from_authorized_user_info) to create a new Credentials instance.
    - [`id_token`](https://google-auth.readthedocs.io/en/stable/reference/google.oauth2.credentials.html#google.oauth2.credentials.Credentials.id_token): can be verified and decoded (parsed) using [`google.oauth2.id_token.verify_oauth2_token()`](https://google-auth.readthedocs.io/en/stable/reference/google.oauth2.id_token.html#google.oauth2.id_token.verify_oauth2_token)
    
- **Featured Google OAuth implementations and libraries:**
    - 📦 **`oauth2client`** ([googleapis/oauth2client](https://github.com/googleapis/oauth2client)):   ***deprecated*** in favor of **`google-auth`**.<br>
           `💻 $ pip install --upgrade oauth2client`<br>
           `🐍 from oauth2client.client import GoogleCredentials`

    - 📦 **`google-auth`** ([googleapis/google-auth-library-python](https://github.com/googleapis/google-auth-library-python)): provides the ability to authenticate to Google APIs using various methods. It comprises two sub-packages: [`google.auth`](https://googleapis.dev/python/google-auth/latest/reference/google.auth.html) and [`google.oauth2`](https://googleapis.dev/python/google-auth/latest/reference/google.oauth2.html).<br>
           `💻 $ pip install google-auth`<br>
           `🐍 from google.auth.transport.requests import Request`<br>
           `🐍 from google.oauth2.credentials import Credentials`

    - 📦 **`OAuthLib`** ([oauthlib/oauthlib](https://github.com/oauthlib/oauthlib)): a Python framework which implements the logic of OAuth1 or OAuth2 without assuming a specific HTTP request object or web framework.<br>
           `💻 $ pip install oauthlib`<br>
           `🐍 from oauthlib.oauth2 import WebApplicationClient`
        
    - 📦 **`google-auth-oauthlib`** ([googleapis/google-auth-library-python-oauthlib](https://github.com/googleapis/google-auth-library-python-oauthlib)): used for this project. It contains experimental **`OAuthLib`** integration with **`google-auth`**.<br>
           `💻 $ pip install google-auth-oauthlib`<br>
           `🐍 from google_auth_oauthlib.flow import Flow`

## License

MIT license.
# Google OAuthLib Django

Sample Django project using [`google-auth-oauthlib`](https://github.com/googleapis/google-auth-library-python-oauthlib) for OAuth2 authentication.

<br /><img src="/google-oauthlib-django.gif" alt="google-oauthlib-django.gif" width="500"/><br />

The structure of the code was built upon the [AuthLib library demo for Django](https://github.com/authlib/demo-oauth-client/tree/310c6f1da26abc32f8eca8668d1b6d0aa4a9f0a3/django-google-login) and the [Google Apps Script API Python Quickstart](https://github.com/googleworkspace/python-samples/tree/aacc00657392a7119808b989167130b664be5c27/apps_script/quickstart) (and later, the [Drive V3 Python Quickstart](https://github.com/googleworkspace/python-samples/tree/master/drive/quickstart), for simpler API calls):

- **[AuthLib](https://github.com/lepture/authlib)** would have been my goto library, but I dropped it after many tries, due to confusing instructions about OAuth2 refresh token support for Django _(at least, up until February 2021)_:
    - _[python - Getting refresh_token with lepture/authlib - Stack Overflow](https://stackoverflow.com/questions/48907773/getting-refresh-token-with-lepture-authlib)_
        - > _`client_credentials` won't issue refresh token. You need to use authorization_code flow to get the refresh token._
            - _A OAuth server-side configuration seems to be needed: [stackoverflow.com/questions/51305430/…](https://stackoverflow.com/questions/51305430/obtaining-refresh-token-from-lepture-authlib-through-authorization-code/51305975#51305975)_
    - _[Refresh and Auto Update Token · Issue #245 · lepture/authlib](https://github.com/lepture/authlib/issues/245)_
        - > _Also be aware, unless you're on authlib 0.14.3 or later, the django integration is broken for refresh (If you're using the metadata url): [RemoteApp.request fails to use token_endpoint to refresh the access token · Issue #193 · lepture/authlib](https://github.com/lepture/authlib/issues/193)_

- ***Google AppsScript/Drive API Python Quickstart*** code adaptation:
    - `credentials.json` contains [OAuth client ID credentials](https://developers.google.com/identity/protocols/oauth2/web-server#creatingcred) of the GCP project, that will provide access to Google user's resources for the Django app.
    - [`Flow`](https://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html#google_auth_oauthlib.flow.Flow) class was used instead of [`InstalledAppFlow`](https://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html#google_auth_oauthlib.flow.InstalledAppFlow).
    - Instead of using pickles, OAuth2 token (a [`Credentials`](https://google-auth.readthedocs.io/en/stable/reference/google.oauth2.credentials.html#google.oauth2.credentials.Credentials) instance) is converted to a dictionary and saved to the session (as a session key named `token`).
    - Value of session key `user` (which identifies the logged in user) is retrieved by [parsing](https://google-auth.readthedocs.io/en/stable/reference/google.oauth2.id_token.html#google.oauth2.id_token.verify_oauth2_token) the [Open ID Connect ID Token](https://google-auth.readthedocs.io/en/stable/reference/google.oauth2.credentials.html#google.oauth2.credentials.Credentials.id_token) contained in the Credentials object resulting from a complete and successful OAuth2 flow.

- Added a few features:
    - Handling backend errors, warnings and infos, and storing their respective messages to the session key `messages`, which is added as a variable to template's context, and then rendered on the frontend.
    - Handling access to some special paths like `/login` and `/auth` (no `404` catch-all page, though).

## Setup

_Tested and run on Windows 10 x64, with `Python 3.9.1`:_

- Create a GCP project, enable Drive API, add the following scopes and then download webapp Client ID credentials file from the GCP console:

    ```
    'https://www.googleapis.com/auth/drive', \
    'https://www.googleapis.com/auth/userinfo.email', \
    'https://www.googleapis.com/auth/userinfo.profile', \
    'openid'
    ```

- Clone the repository and create a virtual environment:

    ```bash
    git clone git@github.com:amindeed/Google-OAuthLib-Django.git
    cd Google-OAuthLib-Django
    virtualenv venv
    source venv/Scripts/activate
    ```

- Install required libraries, create Django database and launch the dev server:

    ```bash
    pip install Django google-api-python-client google-auth-oauthlib
    ## OR: 'pip install -r requirements.txt'
    # Migrate changes to Django's DB (only in first time run)
    python manage.py migrate
    python manage.py runserver
    ```

## Background

The code in this repository was a result of my researches for another project: [`GMail-AutoResponder`](https://github.com/amindeed/Gmail-AutoResponder/blob/master/worklog.md#2021-02-15-code).

## License

MIT license.
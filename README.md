# Google OAuthLib Django Quickstart

Sample Django project using [`google-auth-oauthlib`](https://github.com/googleapis/google-auth-library-python-oauthlib) for OAuth2 authentication.

## Setup

Tested and run on Windows 10 x64, with `Python 3.9.1`:

```bash
git clone git@github.com:amindeed/Google-OAuthLib-Django-Quickstart.git
cd Google-OAuthLib-Django-Quickstart/{PROJECT-DIRECTORY}
virtualenv venv
source venv/Scripts/activate
pip install Django google-api-python-client google-auth-oauthlib python-dotenv
## OR: 'pip install -r requirements.txt'
# Migrate changes to Django's DB (only in first time run)
python manage.py migrate
python manage.py runserver
```
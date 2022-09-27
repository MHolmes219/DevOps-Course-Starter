import os, requests


def get_access_token(CLIENT_ID: str, CLIENT_SECRET: str, request_token: str) -> str:
    if not CLIENT_ID:
        raise ValueError('The CLIENT_ID has to be supplied!')
    if not CLIENT_SECRET:
        raise ValueError('The CLIENT_SECRET has to be supplied!')
    if not request_token:
        raise ValueError('The request token has to be supplied!')
    if not isinstance(CLIENT_ID, str):
        raise ValueError('The CLIENT_ID has to be a string!')
    if not isinstance(CLIENT_SECRET, str):
        raise ValueError('The CLIENT_SECRET has to be a string!')
    if not isinstance(request_token, str):
        raise ValueError('The request token has to be a string!')

    url = f'https://github.com/login/oauth/access_token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&code={request_token}'
    headers = {
        'accept': 'application/json'
    }

    res = requests.post(url, headers=headers)

    data = res.json()
    access_token = data['access_token']

    return access_token


def get_user_data(access_token: str) -> dict:

    if not access_token:
        raise ValueError('The request token has to be supplied!')
    if not isinstance(access_token, str):
        raise ValueError('The request token has to be a string!')

    access_token = 'token ' + access_token
    url = 'https://api.github.com/user'
    headers = {"Authorization": access_token}

    resp = requests.get(url=url, headers=headers)

    userData = resp.json()

    return userData

class Config:
    def __init__(self):
        """Base configuration variables."""
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        if not self.SECRET_KEY:
            raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")

        self.ENDPOINT = os.environ.get('ENDPOINT')
        self.DATABASE = os.environ.get('DATABASE')
        self.CLIENT_ID = os.environ.get('CLIENT_ID')
        self.CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
        self.STATE = os.environ.get('STATE')
        self.LOGIN_DISABLED = os.getenv('LOGIN_DISABLED') == 'True'

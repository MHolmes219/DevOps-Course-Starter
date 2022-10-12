import requests

class UserAccess:
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
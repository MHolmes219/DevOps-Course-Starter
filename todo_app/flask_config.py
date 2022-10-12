import os

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

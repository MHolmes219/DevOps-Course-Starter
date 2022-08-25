import os


class Config:
    def __init__(self):
        """Base configuration variables."""
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        if not self.SECRET_KEY:
            raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")
        self.BASE_URL = 'https://api.trello.com/1'
        self.API_KEY = os.environ.get('API_KEY')
        self.API_TOKEN = os.environ.get('API_TOKEN')
        self.BOARD_ID = os.environ.get('BOARD_ID')

        self.ENDPOINT = os.environ.get('ENDPOINT')
        self.DATABASE = os.environ.get('DATABASE')

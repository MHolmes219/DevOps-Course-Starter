from flask import Flask, render_template, request, redirect, url_for, Blueprint, session
from todo_app.data import trello_items as items
from todo_app.view_model import ViewModel
from todo_app.flask_config import Config
from todo_app.oauth_helpers import UserAccess
from flask_login import LoginManager, login_required, UserMixin, login_user, current_user
import string, random
from functools import wraps
from loggly.handlers import HTTPSHandler
from pythonjsonlogger import jsonlogger
from logging import getLogger


def user_authorised(func):
    '''Check user role access'''

    @wraps(func)
    def auth_wrapper(*args, **kwargs):
        print(f'Function: {func.__name__}')
        print(f'{"-"*30}')
        if current_user.role != "writer":
            return "Forbidden", 403
        return func(*args, **kwargs)
    return auth_wrapper

class User(UserMixin):
    def __init__(self, id):
        self.id = id
    
    @property
    def role(self):
        if self.id == '94120411':
            return "writer"
        else:
            return "reader"


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config())

    app.logger.setLevel(app.config['LOG_LEVEL'])

    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthenticated():
        state = string.digits
        stateString = ''.join(random.choice(state) for i in range(20))
        session['user-state'] = stateString
        app.logger.info("User is unauthenticated")
        return redirect('https://github.com/login/oauth/authorize?client_id=' + app.config['CLIENT_ID'] + '&state=' + stateString)

    @login_manager.user_loader
    def load_user(user_id):
        app.logger.info("User is authenticated and their role is %s", User(user_id).role)
        return User(user_id)
    
    login_manager.init_app(app)

    if app.config['LOGGLY_TOKEN'] is not None:
        handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{app.config["LOGGLY_TOKEN"]}/tag/todo-app')
        werkzeugHandler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{app.config["LOGGLY_TOKEN"]}/tag/todo-app-requests')

        handler.setFormatter(
            jsonlogger.JsonFormatter("%(asctime)s %(module)s %(levelname)s %(message)s")
        )
        
        getLogger('werkzeug').addHandler(werkzeugHandler)
        app.logger.addHandler(handler)


    @app.route('/login/callback', methods=['GET'])
    def login_callback():
        """Authenticate the user and displays their data."""
        args = request.args
        returedState = args.get('state')
        sessionState = session.get('user-state')
        request_token = args.get('code')

        CLIENT_ID = app.config['CLIENT_ID']
        CLIENT_SECRET = app.config['CLIENT_SECRET']
        access_token = UserAccess.get_access_token(CLIENT_ID, CLIENT_SECRET, request_token)

        user_data = UserAccess.get_user_data(access_token)

        if returedState == sessionState:
            login_user(User(user_data['id']))

        return redirect(url_for('index'))


    # Define the index page and display all sorted cards
    @app.route('/')
    @login_required
    def index():

        allCards = items.get_cards()

        item_view_model = ViewModel(allCards)

        return render_template('index.html', view_model=item_view_model)


    # Add a new card to the list
    @app.route('/add-card', methods=["POST"])
    @login_required
    @user_authorised
    def new_card():

        name = request.form.get('name')
        desc = request.form.get('desc')
        due = request.form.get('due-date')
        items.add_card(name, desc, due)

        return redirect(url_for('index')) 


    # View individual card using card id
    @app.route('/view-card/<cardId>')
    @login_required
    def view_card(cardId):
        card = items.get_card(cardId)

        app.logger.info("Current card: %s", card[0]['name'])

        return render_template('view_card.html', card = card)


    # Update card status to In Progress
    @app.route('/start-card/<cardId>', methods=["POST"])
    @login_required
    @user_authorised
    def start_card(cardId):

        items.start_card(cardId)

        app.logger.info('Card %s started', cardId)

        return redirect(url_for('index'))


    # Update card status to Done
    @app.route('/complete-card/<cardId>', methods=["POST"])
    @login_required
    @user_authorised
    def complete_card(cardId):

        items.complete_card(cardId)

        app.logger.info('Card %s completed', cardId)

        return redirect(url_for('index'))


    # Update card status to To Do
    @app.route('/undo-card/<cardId>', methods=["POST"])
    @login_required
    @user_authorised
    def undo_card(cardId):

        items.undo_card(cardId)

        app.logger.info('Card %s restarted', cardId)

        return redirect(url_for('index'))


    # Delete card
    @app.route('/delete-card/<cardId>', methods=["POST"])
    @login_required
    @user_authorised
    def delete_card(cardId):
            
        items.delete_card(cardId)

        app.logger.info('Card %s deleted', cardId)

        return redirect(url_for('index'))

    return app

if __name__ == '__main__':
    create_app().run()
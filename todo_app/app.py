from flask import Flask, render_template, request, redirect, url_for, Blueprint
from todo_app.data import trello_items as trello
from todo_app.view_model import ViewModel
from todo_app.flask_config import Config
import datetime

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config())
    app.register_blueprint(filters)

    # Define the index page and display all sorted cards
    @app.route('/')
    def index():

        allCards = trello.get_cards()

        item_view_model = ViewModel(allCards)

        return render_template('index.html', view_model=item_view_model)


    # Add a new card to the list
    @app.route('/add-card', methods=["POST"])
    def new_card():
        name = request.form.get('name')
        desc = request.form.get('desc')
        due = request.form.get('due-date')
        trello.add_card(name, desc, due)

        return redirect(url_for('index')) 


    # View individual card using card id
    @app.route('/view-card/<cardId>')
    def view_card(cardId):
        card = trello.get_card(cardId)

        return render_template('index.html', card = card)


    # Update card status to In Progress
    @app.route('/start-card/<cardId>', methods=["POST"])
    def start_card(cardId):
        trello.start_card(cardId)

        return redirect(url_for('index'))


    # Update card status to Done
    @app.route('/complete-card/<cardId>', methods=["POST"])
    def complete_card(cardId):
        trello.complete_card(cardId)

        return redirect(url_for('index'))


    # Update card status to To Do
    @app.route('/undo-card/<cardId>', methods=["POST"])
    def undo_card(cardId):
        trello.undo_card(cardId)

        return redirect(url_for('index'))


    # Archive card
    @app.route('/archive-card/<cardId>', methods=["POST"])
    def archive_card(cardId):
        trello.archive_card(cardId)

        return redirect(url_for('index'))

    return app

if __name__ == '__main__':
    create_app().run()


# Filters
filters = Blueprint('filters', __name__)

def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

@filters.app_template_filter()
def formatted_time(dttm):
    ettm = datetime.datetime.strptime(dttm, "%Y-%m-%dT%H:%M:%S.%fZ")
    return custom_strftime("{S} %B %Y", ettm)
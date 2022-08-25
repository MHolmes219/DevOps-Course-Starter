from flask import Flask, render_template, request, redirect, url_for, Blueprint
from todo_app.data import trello_items as items
from todo_app.view_model import ViewModel
from todo_app.flask_config import Config

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config())

    # Define the index page and display all sorted cards
    @app.route('/')
    def index():

        allCards = items.get_cards()

        item_view_model = ViewModel(allCards)

        return render_template('index.html', view_model=item_view_model)


    # Add a new card to the list
    @app.route('/add-card', methods=["POST"])
    def new_card():
        name = request.form.get('name')
        desc = request.form.get('desc')
        due = request.form.get('due-date')
        items.add_card(name, desc, due)

        return redirect(url_for('index')) 


    # View individual card using card id
    @app.route('/view-card/<cardId>')
    def view_card(cardId):
        card = items.get_card(cardId)

        return render_template('view_card.html', card = card)


    # Update card status to In Progress
    @app.route('/start-card/<cardId>', methods=["POST"])
    def start_card(cardId):
        items.start_card(cardId)

        return redirect(url_for('index'))


    # Update card status to Done
    @app.route('/complete-card/<cardId>', methods=["POST"])
    def complete_card(cardId):
        items.complete_card(cardId)

        return redirect(url_for('index'))


    # Update card status to To Do
    @app.route('/undo-card/<cardId>', methods=["POST"])
    def undo_card(cardId):
        items.undo_card(cardId)

        return redirect(url_for('index'))


    # Delete card
    @app.route('/delete-card/<cardId>', methods=["POST"])
    def delete_card(cardId):
        items.delete_card(cardId)

        return redirect(url_for('index'))

    return app

if __name__ == '__main__':
    create_app().run()
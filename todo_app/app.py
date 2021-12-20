from flask import Flask, render_template, request, redirect, url_for
from todo_app.data import trello_items as trello
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())

# Define the index page and display all sorted cards
@app.route('/')
def index():

    allCards = trello.get_cards()

    return render_template('index.html', allCards = allCards)


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
    

if __name__ == '__main__':
    app.run()
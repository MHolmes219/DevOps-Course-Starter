from flask import Flask, render_template, request, redirect, url_for, session
from todo_app.data.session_items import get_items, add_item, get_item, save_item, remove_item
from todo_app.flask_config import Config
from operator import itemgetter

app = Flask(__name__)
app.config.from_object(Config())


# Define the index page and display all sorted items
@app.route('/')
def index():
    all_items = get_items()

    all_items = sorted(all_items, key=itemgetter('status'), reverse=True)

    return render_template('index.html', all_items = all_items)


# Add a new item to the list
@app.route('/add-item', methods=["POST"])
def new_item():
    title = request.form.get('title')
    add_item(title)

    return redirect(url_for('index'))


# View individual item using item id
@app.route('/view-item/<id>')
def view_item(id):
    view_item = get_item(id)

    return render_template('index.html', item = view_item)


# Update item status to completed
@app.route('/complete-item/<id>', methods=["POST"])
def complete_item(id):

    current_item = get_item(id)

    current_item.update(status='Completed')

    save_item(current_item)

    return redirect(url_for('index'))


# Remove item from list
@app.route('/remove-item/<id>', methods=["POST"])
def delete_item(id):

    current_item = get_item(id)

    remove_item(current_item)

    return redirect(url_for('index'))
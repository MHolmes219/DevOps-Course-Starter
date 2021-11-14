from flask import Flask, render_template, request, redirect
from todo_app.data.session_items import get_items, add_item
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    all_items = get_items()
    return render_template('index.html', all_items = all_items)

@app.route('/add-item', methods=["POST"])
def new_item():
    title = request.form.get('title')
    add_item(title)

    return redirect("/")

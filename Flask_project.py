from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash
import sqlite3
from contextlib import closing

DATABASE = "database.db"
DEBUG = True
SECRET_KEY = 'key'
USERNAME="admin"
PASSWORD="admin"

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

#init_db()

@app.route('/')
def index():
    return render_template("index.html")

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()

from flask import Flask, url_for, g, jsonify, request, redirect
import logging, inspect
import sqlite3
from flask import render_template

# configuration
DATABASE = 'db/auth.db'
DEBUG = False
SECRET_KEY = 'assfdsdfscjhjeaoidpcmi8rhsyfudhwvjdfsn'
USERNAME = 'jllis'
PASSWORD = 'aprimadoandre'


app = Flask(__name__)
app.config.from_object(__name__)

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

@app.before_request
def before_request():
    g.db = get_db()


@app.route('/login')
def inj():
    try:
        query = "select * from users where username='%s' and secret='%s'"
        query = query % (request.args.get('user', ''),request.args.get('pass', ''))
        cur = g.db.execute(query)

        got = cur.fetchall()
        # print 'got:', got
        if got:
            return render_template('inside.html')
        else:
            print 'redirected'
            return redirect('/')

    except Exception as e:
        logging.exception('Exception: FUNCTION: '+inspect.stack()[0][3]+'('+inspect.stack()[1][3]+')')
        return '{}'


@app.route('/')
def noinj():
    try:
        return render_template('index.html')
    except Exception as e:
        logging.exception('Exception: FUNCTION: '+inspect.stack()[0][3]+'('+inspect.stack()[1][3]+')')
        return '{}'

from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import config
import json
import requests

# connect to postgresql database
cur = config.connect()

# Oxford API credentials
app_id = '4edc5d8e'
app_key = 'e359c6bc00f91e8df82211bdf3199eab'
language_code = 'en-us'
endpoint = 'entries'

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

@app.route('/', methods=["POST", "GET"])
def login():
    error = None
    if request.method == 'POST':
        username = str(request.form.get('username')).strip()
        password = str(request.form.get('password')).strip()
        # Retrieving data
        try:
            cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        except Exception as e:
            error = str(e)
        results = cur.fetchone()
        db_user = results[1].strip()
        db_pass = results[4].strip()
        db_id = results[0]
        session['user_id'] = db_id
        if password != db_pass or username != db_user:
            error = 'Invalid username and password, please try again'
        else:
            return redirect(url_for('index', user=db_user))
    return render_template('login.html', error=error)

@app.route('/index')
def index():
    username = request.args['user']
    user_info = {
        'name': username,
        'id': session.get('user_id', None)
    }
    # get user's current lists if they have any
    try:
        cur.execute("SELECT listname FROM list_items RIGHT OUTER JOIN user_list ON (list_items.listitem_id = user_list.listitem_id)")
    except Exception as e:
        print(e)

    results = cur.fetchall()
    lists = []
    for vocab_list in results:
        lists.append(vocab_list[0].strip())

    return render_template('index.html', user=user_info, lists=lists)

@app.route('/createlist', methods=["POST", "GET"])
def create_list():
    error = None
    user_id = session.get('user_id', None)
    if request.method == 'POST':
        vocab_list = str(request.form.get('words')).strip()
        list_name = str(request.form.get('listname')).strip()
        if vocab_list == "" or list_name == "":
            error = 'Cannot have an empty list or empty list name'
        else:
            return redirect(url_for('new_list', vocab_list=vocab_list, list_name=list_name))
    return render_template('create_list.html', error=error)

@app.route('/newlist', methods=["POST", "GET"])
def new_list():
    error = None
    vocab = request.args['vocab_list']
    listname = request.args['list_name']
    words = vocab.split(',')
    # first check/update our cache 
    cache = {}
    try:
        cur.execute("SELECT * FROM oxford_cache")
    except Exception as e:
            print(e)
    results = cur.fetchall()
    for item in results:
        word_definition = item[2].strip()
        word = item[1].strip()
        cache[word] = word_definition

    definitions = dict()
    for word in words:
        if word in cache:
            word_definition = ''.join(c for c in cache[word] if c not in '{}""')
            definitions[word] = word_definition
        else:
            word_id = word.lower().strip()
            url = 'https://od-api.oxforddictionaries.com/api/v2/' + endpoint + '/' + language_code + '/' + word_id
            try:
                r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})
            except Exception as e:
                error = str(e)
            response = r.json()
            definition = response["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"]
            definitions[word] = definition[0]
            cur.execute("INSERT INTO oxford_cache VALUES (DEFAULT, %s, %s)", (word_id, definition))

    listitems = '| '.join("{0} = {1}".format(key,val) for (key,val) in definitions.items())
    # insert into list_items table (flattened definitions dict into a string)
    try:
        cur.execute("INSERT INTO list_items VALUES (DEFAULT, %s, %s)", (listname, listitems))
    except Exception as e:
        print(e)

    # get list id of list inserted above
    try:
        cur.execute("SELECT listitem_id FROM list_items WHERE listname = '{0}'".format(listname))
    except Exception as e:
        print(e)
    res = cur.fetchone()
    list_id = res[0]
    # insert into user_list table with list ID from previous insertion
    user_id = session.get('user_id', None)
    try:
        cur.execute("INSERT INTO user_list VALUES (%s, %s)",(int(user_id), int(list_id)))
    except Exception as e:
        print(e)

    return render_template('vocab_list.html', words=words, listname=listname, definitions=definitions, error=error)

@app.route('/signup', methods=["POST", "GET"])
def signup():
    user_error = None
    password_error = None
    success = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        if len(username) < 5:
            user_error = 'Username must be at least 5 characters long'
        if len(password) < 3:
            password_error = 'Password must be at least 3 characters long'
        if not user_error and not password_error:
            cur.execute("INSERT INTO users VALUES (DEFAULT, %s, %s, %s, %s)", (username, firstname, lastname, password))
            success = 'Account successfully created! Please click the logo to return to the login page'
    return render_template('signup.html', user_error=user_error, password_error=password_error, success=success)

@app.route('/mylist', methods=["POST","GET"])
def get_list():
    listname = request.args['listname']
    try:
        cur.execute("SELECT listitems FROM list_items WHERE listname = '{0}'".format(listname))
    except Exception as e:
        print(e)
    res = cur.fetchone()
    list_items = res[0]
    definitions = dict((a.strip(), b.strip()) for a, b in (item.split('=') for item in list_items.split('| ')))
    return render_template('my_list.html', definitions=definitions, listname=listname)

if __name__ == '__main__':
    app.run(debug=True)
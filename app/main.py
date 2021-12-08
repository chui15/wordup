from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import config

# connect to postgresql database
cur = config.connect()

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
            cur.execute("SELECT * from users WHERE username = %s AND password = %s", (username, password))
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
    return render_template('index.html', user=user_info)

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
    vocab = request.args['vocab_list']
    listname = request.args['list_name']
    #TO DO: insert function to call oxford API to get definitions for each word to generate list
    return render_template('vocab_list.html', vocab=vocab, listname=listname)

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

if __name__ == '__main__':
    app.run(debug=True)
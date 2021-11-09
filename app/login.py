from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username != 'admin' or password != 'admin':
            error = 'Invalid username and password, please try again'
        else:
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/index')
def index():
    user_info = {
        'name': 'admin'
    }
    return render_template('index.html', user=user_info)

@app.route('/signup', methods=["POST", "GET"])
def signup():
    user_error = None
    password_error = None
    success = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if len(username) < 5:
            user_error = 'Username must be at least 5 characters long'
        if len(password) < 3:
            password_error = 'Password must be at least 3 characters long'
        if not user_error and not password_error:
            success = 'Account successfully created! Please click the logo to return to the login page'
    return render_template('signup.html', user_error=user_error, password_error=password_error, success=success)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def login():
    error = None
    # if request.method == 'POST':
    #     if request.form['username'] != 'admin' or request.form['password'] != 'admin':
    #         error = 'Invalid username and password, please try again'
    #     else:
    #         return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/index')
def index():
    user_info = {
        'name': 'admin'
    }
    return render_template('index.html', user=user_info)

@app.route('/signup')
def signup():
    error = None
    return render_template('signup.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
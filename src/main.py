from flask import Flask, render_template, request, session, redirect, url_for
from utils import username_exists, setup_new_user, password_is_wrong
app = Flask(__name__)

app.secret_key = 'software_engineering'

@app.route('/')
def index():
    return render_template("welcome.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username:                            # Empty username
            return 'Username must not be empty'
        elif not username_exists(username):         # Username does not exist
            return 'Username does not exist'
        elif password_is_wrong(username, password): # Wrong password
            return 'Wrong password'
        else:
            session['username'] = username
            return redirect(url_for('diary'))
    else:
        return render_template("login_create.html",
        title="Login", 
        submit_value="Login")

@app.route('/create', methods=["GET", "POST"])
def create():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username:                            # Empty username
            return 'Username must not be empty'
        elif username_exists(username):             # Username already exists
            return 'Username already exists'
        elif len(password) < 5:                     # Password is too short
            return 'Password is too short'
        else:                                       # Everything is good
            setup_new_user(username, password)
            session['username'] = username
            return redirect(url_for('diary'))
    else:
        return render_template("login_create.html",
        title="Create an account", 
        submit_value="Create")

@app.route('/diary')
def diary():
    if 'username' in session:                       # User is logged in
        return 'Welcome, %s!' %session['username']
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, session, redirect, url_for
from controller import username_exists, setup_new_user, password_is_wrong, load_diary_instances_for_username, add_text_to_users_diary, add_picture_to_users_diary, delete_text_from_users_diary, delete_picture_from_users_diary, edit_text_in_users_diary
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
        if not username:                                                # Empty username
            return 'Username must not be empty'
        elif not username_exists(username):                             # Username does not exist
            return 'Username does not exist'
        elif password_is_wrong(username, password):                     # Wrong password
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
        if not username:                                                # Empty username
            return 'Username must not be empty'
        elif username_exists(username):                                 # Username already exists
            return 'Username already exists'
        elif len(password) < 5:                                         # Password is too short
            return 'Password is too short'
        else:                                                           # Everything is good
            setup_new_user(username, password)
            session['username'] = username
            return redirect(url_for('diary'))
    else:
        return render_template("login_create.html",
        title="Create an account", 
        submit_value="Create")

@app.route('/diary')
def diary():
    if 'username' not in session:
        return redirect(url_for('index'))                               # User is logged in
    username = session['username']
    diary_instances = load_diary_instances_for_username(username)
    return render_template("diary.html",
    username = username,
    diary_instances=diary_instances,
    enumerate=enumerate)
    
@app.route('/add/text', methods=["GET", "POST"])
def add_text():
    if 'username' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = session['username']
        text_to_add = request.form['text']
        add_text_to_users_diary(username, text_to_add)
        return redirect(url_for('diary'))
    else:
        return render_template("add_text.html")

@app.route('/add/picture', methods=["GET", "POST"])
def add_picture():
    if 'username' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = session['username']
        picture_to_add = request.files['picture']
        add_picture_to_users_diary(username, picture_to_add)
        return redirect(url_for('diary'))
    else:
        return render_template("add_picture.html")

@app.route('/delete/text/<int:diary_index>')
def delete_text(diary_index):
    if 'username' not in session:
        return redirect(url_for('index'))
    username = session['username']
    delete_text_from_users_diary(username, diary_index)
    return redirect(url_for('diary'))

@app.route('/delete/picture/<int:diary_index>')
def delete_picture(diary_index):
    if 'username' not in session:
        return redirect(url_for('index'))
    username = session['username']
    delete_picture_from_users_diary(username, diary_index)
    return redirect(url_for('diary'))

@app.route('/edit/text/<int:diary_index>', methods=["GET", "POST"])
def edit_text(diary_index):
    if 'username' not in session:
        return redirect(url_for('index'))
    username = session['username']
    if request.method == 'POST':
        text_to_save = request.form['text']
        edit_text_in_users_diary(username, text_to_save, diary_index)
        return redirect(url_for('diary'))
    else:
        diary_instances = load_diary_instances_for_username(username)
        return render_template("edit_text.html",
        diary_instance=diary_instances[diary_index],
        diary_index=diary_index)
    
@app.route('/edit/picture/<int:diary_index>', methods=["GET", "POST"])
def edit_picture(diary_index):
    if 'username' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = session['username']
        picture_to_add = request.files['picture']
        add_picture_to_users_diary(username, picture_to_add)
        return redirect(url_for('diary'))
    else:
        return render_template("edit_picture.html")
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
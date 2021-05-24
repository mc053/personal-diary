import os
import json
from datetime import datetime
import uuid
from werkzeug.utils import secure_filename
from model import TextEntry, PictureEntry
from flask import url_for, redirect

# Files inside the user's folder
password_file_name = "password.txt"
diary_file_name = "diary.json"

date_format = "%B %d, %Y %H:%M:%S"

def username_exists(username):
    return os.path.exists(get_user_path(username))

def setup_new_user(username, password):
    # Create user's folder
    user_path = get_user_path(username)
    os.makedirs(user_path)

    complete_password_file_name = os.path.join(user_path, password_file_name)
    complete_diary_file_name = os.path.join(user_path, diary_file_name)

    # Write password into password.txt
    file = open(complete_password_file_name, "w")
    file.write(password)
    file.close()

    # Diary is an empty array at the beginning
    file = open(complete_diary_file_name, "w")
    file.write("[]")
    file.close()

def load_diary_instances_for_username(username):
    diary_path = get_users_diary_path(username)
    diary_instances = []

    with open(diary_path) as file:
        diary_entries = json.load(file)

#    diary_entries = sorted(diary_entries,
#    key=lambda entry: datetime.strptime(entry['date'], date_format),
#    reverse=True)

    for diary_entry in diary_entries:
        if diary_entry['entryType'] == TextEntry.__name__:
            diary_instances.append(TextEntry(diary_entry['date'],
            diary_entry['content']))
        elif diary_entry['entryType'] == PictureEntry.__name__:
            diary_instances.append(PictureEntry(diary_entry['date'],
            url_for('static', filename=diary_entry['content'])))

    return diary_instances

def add_text_to_users_diary(username, text_to_add):
    entry_to_add = {
        "date": datetime.now().strftime(date_format),
        "content": text_to_add,
        "entryType": "TextEntry"
    }
    add_entry_to_users_diary(username, entry_to_add)
    
def add_picture_to_users_diary(username, picture_to_add):
    picture_format = "." + picture_to_add.filename.split('.')[1]
    # In case there are different pictures with same name
    unique_filename = str(uuid.uuid4()) + picture_format
    picture_to_add.save(get_dir_path() + "/static/user_pictures/" + secure_filename(unique_filename))

    entry_to_add = {
        "date": datetime.now().strftime(date_format),
        "content": "user_pictures/" + unique_filename,
        "entryType": "PictureEntry"
    }
    add_entry_to_users_diary(username, entry_to_add)

def add_entry_to_users_diary(username, entry_to_add):
    diary_path = get_users_diary_path(username)

    with open(diary_path) as file:
        diary_entries = json.load(file)

    diary_entries.insert(0, entry_to_add)

    with open(diary_path, mode='w') as file:
        file.write(json.dumps(diary_entries))

def delete_text_from_users_diary(username, diary_index):
    diary_path = get_users_diary_path(username)

    with open(diary_path) as file:
        diary_entries = json.load(file)

    diary_entries.pop(diary_index)

    with open(diary_path, mode='w') as file:
        file.write(json.dumps(diary_entries))

def delete_picture_from_users_diary(username, diary_index):
    diary_path = get_users_diary_path(username)

    with open(diary_path) as file:
        diary_entries = json.load(file)

    entry_to_delete = diary_entries[diary_index]
    picture_to_delete = entry_to_delete['content']
    os.remove(get_dir_path() + "/static/" + picture_to_delete)

    diary_entries.pop(diary_index)

    with open(diary_path, mode='w') as file:
        file.write(json.dumps(diary_entries))

def edit_text_in_users_diary(username, text_to_save, diary_index):
    diary_path = get_users_diary_path(username)

    with open(diary_path) as file:
        diary_entries = json.load(file)

    old_entry = diary_entries[diary_index]
    new_entry = {
        "date": old_entry['date'],
        "content": text_to_save,
        "entryType": "TextEntry"
    }
    
    diary_entries.pop(diary_index)
    diary_entries.insert(diary_index, new_entry)

    with open(diary_path, mode='w') as file:
        file.write(json.dumps(diary_entries))    

def password_is_wrong(username, password):
    complete_password_file_name = os.path.join(get_user_path(username), password_file_name)
    password_file = open(complete_password_file_name, "r")
    password_file_content = password_file.read()
    password_file.close()

    return password != password_file_content

def check_if_user_is_logged_in(session):
    if 'username' not in session:
        return redirect(url_for('index'))

def get_users_diary_path(username):
    return get_user_path(username) + "/diary.json"

def get_user_path(username):
    return get_dir_path() + "/users/" + username

def get_dir_path():
    return os.path.dirname(os.path.realpath(__file__))
import os

def username_exists(username):
    return os.path.exists(dir_path() + "/users/" + username)

def setup_new_user(username, password):
    # Create user's folder with a pictures-subfolder inside it
    user_path = dir_path() + "/users/" + username
    os.makedirs(user_path)
    os.makedirs(user_path + "/pictures")

    # We need these two initial files inside the user's folder
    passwordFileName = "password.txt"
    diaryFileName = "diary.json"

    completePasswordFileName = os.path.join(user_path, passwordFileName)
    completeDiaryFileName = os.path.join(user_path, diaryFileName)

    # Write password into password.txt (Not really secure, I know...)
    file = open(completePasswordFileName, "w")
    file.write(password)
    file.close()

    # Diary is an empty array at the beginning
    file = open(completeDiaryFileName, "w")
    file.write("[]")
    file.close()

def dir_path():
    return os.path.dirname(os.path.realpath(__file__))

def password_is_wrong(username, password):
    pass
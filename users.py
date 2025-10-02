from werkzeug.security import check_password_hash, generate_password_hash

import db


def get_username(user_id):
    try:
        sql = "SELECT username FROM users WHERE id = ?"
        return db.query(sql, [user_id])[0][0]
    except:
        return None


def create_user(username, password):
    password_hash = generate_password_hash(password)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
        return db.last_insert_id()
    except:
    # except sqlite3.IntegrityError:
        return None


def check_login(username, password):
    try:
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        user_id, password_hash = db.query(sql, [username])[0]
    except:
        return None

    # deal with test users from init.sql for which no password hash is stored
    if password_hash is None:
        return None

    if check_password_hash(password_hash, password) is False:
        return None

    return user_id

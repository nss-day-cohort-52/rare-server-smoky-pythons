import sqlite3
import json
from datetime import datetime
from models import User

def login_user(user):
    """Checks for the user in the database

    Args:
        user (dict): Contains the username and password of the user trying to login

    Returns:
        json string: If the user was found will return valid boolean of True and the user's id as the token
                     If the user was not found will return valid boolean False
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            select id, username
            from Users
            where username = ?
            and password = ?
        """, (user['username'], user['password']))

        user_from_db = db_cursor.fetchone()

        if user_from_db is not None:
            response = {
                'valid': True,
                'token': user_from_db['id']
            }
        else:
            response = {
                'valid': False
            }

        return json.dumps(response)

def get_all_users():
    """Returns all the users from the server as a list of dictionaries"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Select *
        FROM Users
        ORDER BY username ASC             
        """)

        dataset = db_cursor.fetchall()

        users = []

        for row in dataset:
            user = User(row['id'], row['first_name'], row['last_name'],
                        row['username'], row['email'], row['password'], row['bio'])
            users.append(user.__dict__)

        return json.dumps(users)

def get_single_user(id):
    """Returns a single user from the server"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            u.id, 
            u.first_name, 
            u.last_name, 
            u.username, 
            u.email, 
            u.password, 
            u.bio
        FROM Users u 
        WHERE u.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        user = User(data['id'],data['first_name'],data['last_name'],
                    data['username'],data['email'],data['password'],data['bio'])

        return json.dumps(user)

def create_user(user):
    """Adds a user to the database when they register

    Args:
        user (dictionary): The dictionary passed to the register post request

    Returns:
        json string: Contains the token of the newly created user
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Insert into Users (first_name, last_name, username, email, password, bio, created_on, active) values (?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            user['first_name'],
            user['last_name'],
            user['username'],
            user['email'],
            user['password'],
            user['bio'],
            datetime.now()
        ))

        id = db_cursor.lastrowid

        return json.dumps({
            'token': id,
            'valid': True
        })

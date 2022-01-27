import sqlite3
import json
from datetime import datetime
from models import Subs

def get_all_subscriptions():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT * FROM Subscriptions                  
        """)

        subscriptions = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            subscription = Subs(row['id'], row['follower_id'], row['author_id'], row['created_on'])
            subscriptions.append(subscription.__dict__)

        return json.dumps(subscriptions)
def get_users_subscriptions(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            s.id,
            s.follower_id, 
            s.author_id, 
            s.created_on
        FROM Subscriptions s 
        WHERE s.follower_id = ?
        """, (id, ))
        
        subs = []
        
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            sub = Subs(row['id'],row['follower_id'],row['author_id'],
                    row['created_on'])
            subs.append(sub.__dict__)
        return json.dumps(subs)
    
def create_subscription(new_subscription):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Subscriptions
            (follower_id, author_id, created_on)
        VALUES
            (?,?,?);
        """, (new_subscription['followerId'],new_subscription['authorId'],new_subscription['createdOn']))

        id = db_cursor.lastrowid

        new_subscription['id'] = id

    return json.dumps(new_subscription)

def delete_subscription(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Subscriptions
        WHERE id = ?
        """, (id, ))
import json
import sqlite3

from models import Post


def get_all_posts():
    """Returns all the posts from the server as a list of dictionaries"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select * from Posts                  
        """)

        dataset = db_cursor.fetchall()

        posts = []

        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'],
                        row['title'], row['publication_date'], row['content'])

            posts.append(post.__dict__)

        return json.dumps(posts)


def get_single_post(id):
    """Returns a single post from the server as a dictionary"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select * from Posts
        where id = ?                  
        """, (id, ))

        data = db_cursor.fetchone()

        post = Post(data['id'], data['user_id'], data['category_id'],
                    data['title'], data['publication_date'], data['content'])

        return json.dumps(post.__dict__)

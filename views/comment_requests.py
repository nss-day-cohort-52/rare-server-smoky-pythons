import json
import sqlite3
from models import Comment


def get_all_comments():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select * from comments                  
        """)

        comments = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            comment = Comment(row['id'], row['author_id'],
                              row['post_id'], row['content'])

            comments.append(comment.__dict__)

        return json.dumps(comments)


def get_single_comment(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select * from comments
        where id = ?                  
        """, (id, ))

        data = db_cursor.fetchone()

        comment = Comment(data['id'], data['author_id'],
                          data['post_id'], data['content'])

        return json.dumps(comment.__dict__)


def add_comment(comment):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        insert into comments (post_id, author_id, content)
        values (?, ?, ?)
        """, (comment['postId'], comment['authorId'], comment['content']))

        id = db_cursor.lastrowid
        comment['id'] = id

        return json.dumps(comment)


def delete_comment(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        delete from Comments
        where id = ?
        """, (id, ))

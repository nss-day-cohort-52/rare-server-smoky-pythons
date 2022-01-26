import json
import sqlite3

from models import Tag


def get_all_tags():
    """Retrieve category list
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            a.id, 
            a.label
        FROM Tags a 
        """)

        tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            tag = Tag(row['id'], row['label'])

            tags.append(tag.__dict__)

    return json.dumps(tags)


def get_single_tag(id):
    """Retrieve single tag
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            a.id, 
            a.label
        FROM Tags a 
        WHERE a.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        tag = Tag(data['id'], data['label'])

    return json.dumps(tag.__dict__)


def find_tag(search_tag):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            a.id,
            a.label
        FROM Tags a
        WHERE a.label LIKE ? 
        """, (search_tag, ))

        tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            tag = Tag(row['id'],
                                row['label'])

            tags.append(tag.__dict__)

    # Use `json` package to properly serialize list as JSON
    # json.dumps() function converts a Python object into a json string.
    return json.dumps(tags)


def create_tag(new_tag):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Tags
            (label)
        VALUES
            (?);
        """, (new_tag['label'], ))

        id = db_cursor.lastrowid

        new_tag['id'] = id

    return json.dumps(new_tag)
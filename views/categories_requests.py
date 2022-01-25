import json
import sqlite3

from models import Category


def get_all_categories():
    """Retrieve category list
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            a.id, 
            a.label
        FROM Categories a 
        """)

        categories = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            category = Category(row['id'], row['label'])

            categories.append(category.__dict__)

    return json.dumps(categories)


def get_single_category(id):
    """Retrieve single category
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            a.id, 
            a.label
        FROM Categories a 
        WHERE a.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        category = Category(data['id'], data['label'])

    return json.dumps(category.__dict__)


def find_category(search_category):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            a.id,
            a.label
        FROM Categories a
        WHERE a.label LIKE ? 
        """, (search_category, ))

        categories = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            category = Category(row['id'],
                                row['label'])

            categories.append(category.__dict__)

    # Use `json` package to properly serialize list as JSON
    # json.dumps() function converts a Python object into a json string.
    return json.dumps(categories)


def create_category(new_category):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Categories
            (label)
        VALUES
            (?);
        """, (new_category['label'], ))

        id = db_cursor.lastrowid

        new_category['id'] = id

    return json.dumps(new_category)

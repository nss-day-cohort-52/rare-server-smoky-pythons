import sqlite3
import json
from models import PostTag


def get_all_post_tags():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select * from PostTags                  
        """)

        post_tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            post_tag = PostTag(row['id'], row['post_id'], row['tag_id'])
            post_tags.append(post_tag.__dict__)

        return json.dumps(post_tags)

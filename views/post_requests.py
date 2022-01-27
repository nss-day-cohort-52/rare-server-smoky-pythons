from curses import newpad
import json
import sqlite3

from models import Post
from models.category import Category
from models.tag import Tag
from models.user import User


def get_all_posts():
    """Returns all the posts from the server as a list of dictionaries"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
        p.id,
        p.user_id,
        p.category_id,
        p.title,
        p.publication_date,
        p.content,
        u.first_name,
        u.last_name,
        u.username,
        u.email,
        u.password,
        u.bio,
        u.created_on,
        c. label
        FROM Posts p 
        LEFT JOIN Users u
            on u.id = p.user_id
        LEFT JOIN Categories c 
            on c.id = p.category_id              
        """)

        dataset = db_cursor.fetchall()

        posts = []

        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'],
                        row['title'], row['publication_date'], row['content'])
            user = User(row['id'], row['first_name'], row['last_name'],
                    row['username'], row['email'], row['password'], row['bio'], row['created_on'])
            category = Category(row['id'], row['label'])
            post.user = user.__dict__
            post.category = category.__dict__
            posts.append(post.__dict__)

            db_cursor.execute("""
            select a.id, a.label
            from PostTags ma
            join Tags a on a.id = ma.tag_id
            where ma.post_id = ?
            """, (post.id, ))

            tags = []

            tag_dataset = db_cursor.fetchall()

            for tag_row in tag_dataset:
                tag = Tag(tag_row['id'], tag_row['label'])
                tags.append(tag.__dict__)

                post.tags = tags

        return json.dumps(posts)


def get_single_post(id):
    """Returns a single post from the server as a dictionary"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
        p.id,
        p.user_id,
        p.category_id,
        p.title,
        p.publication_date,
        p.content,
        u.first_name,
        u.last_name,
        u.username,
        u.email,
        u.password,
        u.bio,
        u.created_on,
        c. label
        FROM Posts p 
        LEFT JOIN Users u
            on u.id = p.user_id
        LEFT JOIN Categories c 
            on c.id = p.category_id    
        where p.id = ?                  
        """, (id, ))

        data = db_cursor.fetchone()

        post = Post(data['id'], data['user_id'], data['category_id'],
                    data['title'], data['publication_date'], data['content'])
        user = User(data['id'], data['first_name'], data['last_name'],
                    data['username'], data['email'], data['password'], data['bio'], data['created_on'])
        category = Category(data['id'], data['label'])

        post.user = user.__dict__
        post.category = category.__dict__

        db_cursor.execute("""
            select a.id, a.label
            from PostTags ma
            join Tags a on a.id = ma.tag_id
            where ma.post_id = ?
            """, (post.id, ))

        tags = []

        tag_dataset = db_cursor.fetchall()

        for tag_row in tag_dataset:
            tag = Tag(tag_row['id'], tag_row['label'])
            tags.append(tag.__dict__)

        post.tags = tags

        return json.dumps(post.__dict__)


def create_post(new_post):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts
            ( user_id, category_id, title, publication_date, content )
        VALUES 
            ( ?, ?, ?, ?, ? );
        """, (new_post['user_id'], new_post['category_id'], new_post['title'], new_post['publication_date'], new_post['content'], ))

        id = db_cursor.lastrowid
        new_post['id'] = id

        for tag_id in new_post['tags']:
            db_cursor.execute("""
            insert into PostTags (post_id, tag_id)
            values (?, ?)
            """, (new_post['id'], tag_id))

    return json.dumps(new_post)


def delete_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Posts
        WHERE id = ?
        """, (id, ))


def get_posts_by_user(user):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select 
        p.id,
        p.user_id,
        p.category_id,
        p.title,
        p.publication_date,
        p.content,
        u.first_name,
        u.last_name,
        u.username,
        u.email,
        u.password,
        u.bio,
        u.created_on,
        c. label
        FROM Posts p 
        LEFT JOIN Users u
            on u.id = p.user_id
        LEFT JOIN Categories c 
            on c.id = p.category_id    
        where p.user_id = ?                 
        """, (user, ))

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'],
                        row['title'], row['publication_date'], row['content'])
            user = User(row['id'], row['first_name'], row['last_name'],
                    row['username'], row['email'], row['password'], row['bio'], row['created_on'])
            category = Category(row['id'], row['label'])

            post.user = user.__dict__
            post.category = category.__dict__

            posts.append(post.__dict__)

            db_cursor.execute("""
                select a.id, a.label
                from PostTags ma
                join Tags a on a.id = ma.tag_id
                where ma.post_id = ?
                """, (post.id, ))

            tags = []

            tag_dataset = db_cursor.fetchall()

            for tag_row in tag_dataset:
                tag = Tag(tag_row['id'], tag_row['label'])
                tags.append(tag.__dict__)

                post.tags = tags

        return json.dumps(posts)


def get_posts_by_category(category):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select 
        p.id,
        p.user_id,
        p.category_id,
        p.title,
        p.publication_date,
        p.content,
        u.first_name,
        u.last_name,
        u.username,
        u.email,
        u.password,
        u.bio,
        u.created_on,
        c.label
        FROM Posts p 
        LEFT JOIN Users u
            on u.id = p.user_id
        LEFT JOIN Categories c 
            on c.id = p.category_id    
        where p.category_id = ?                 
        """, (category, ))

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'],
                        row['title'], row['publication_date'], row['content'])
            user = User(row['id'], row['first_name'], row['last_name'],
                    row['username'], row['email'], row['password'], row['bio'], row['created_on'])
            category = Category(row['id'], row['label'])

            post.user = user.__dict__
            post.category = category.__dict__

            posts.append(post.__dict__)

            db_cursor.execute("""
                    select a.id, a.label
                    from PostTags ma
                    join Tags a on a.id = ma.tag_id
                    where ma.post_id = ?
                    """, (post.id, ))

            tags = []

            tag_dataset = db_cursor.fetchall()

            for tag_row in tag_dataset:
                tag = Tag(tag_row['id'], tag_row['label'])
                tags.append(tag.__dict__)

                post.tags = tags

        return json.dumps(posts)

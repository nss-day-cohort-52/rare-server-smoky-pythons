class Post:
    """A class to represent a post"""

    def __init__(self, id, user_id, category_id, title, publication_date, content) -> None:
        self.id = id
        self.user_id = user_id
        self.category_id = category_id
        self.title = title
        self.publication_date = publication_date
        self.content = content

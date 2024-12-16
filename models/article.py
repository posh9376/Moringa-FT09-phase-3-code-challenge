from database.connection import get_db_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        
        self.id=id
        self._title = title
        self._content = content
        self._author_id = author_id
        self._magazine_id = magazine_id


        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO articles ( title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)', ( self._title, self._content, self._author_id, self._magazine_id))
        self._id = cursor.lastrowid
        connection.commit()
        connection.close()

    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not (5 <= len(value) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters.")
        self._title = value

    @property
    def author(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM authors WHERE id = ?;", (self._author_id,))
        author = cursor.fetchone()
        connection.close()
        return author[0]

    @property
    def magazine(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM magazines WHERE id = ?;", (self._magazine_id,))
        magazine = cursor.fetchone()
        connection.close()
        return magazine[0]
    def __repr__(self):
        return f'<Article {self.title}>'

from database.connection import get_db_connection


class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

        # Create a new entry in the database articles table
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO articles (id, title, content, author_id, magazine_id) VALUES (?, ?, ?, ?, ?)', (self.id, self.title, self.content, self.author_id, self.magazine_id))
        conn.commit()
        conn.close()

    @property
    def title(self):
        if hasattr(self, '_title'):
            return self._title
        else:
            # Retrieve the title from the database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT title FROM articles WHERE author_id = ? AND magazine_id = ?', (self.author_id, self.magazine_id))
            result = cursor.fetchone()
            if result:
                self._title = result[0]
            else:
                raise ValueError("Article not found in the database")
            conn.close()
            return self._title

    @title.setter
    def title(self, value):
        if hasattr(self, '_title'):
            raise AttributeError("title cannot be changed after article is instantiated")

        if not isinstance(value, str):
            raise TypeError("title must be a string")
        if len(value) < 5 or len(value) > 50:
            raise ValueError("title must be between 5 and 50 characters, inclusive")

        self._title = value
    
    @property
    def content(self):
        if hasattr(self, '_content'):
            return self.content
        else:
            # Retrieve the content from the database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT content FROM articles WHERE author_id = ? AND magazine_id = ?', (self.author_id, self.magazine_id))
            result = cursor.fetchone()
            if result:
                self._content = result[0]
            else:
                raise ValueError("Article not found in the database")
            conn.close()
            return self._content

    @content.setter
    def content(self, value):
        if hasattr(self, '_content'):
            raise AttributeError("content cannot be changed after article is instantiated")

        if not isinstance(value, str):
            raise TypeError("content must be a string")
        if len(value) < 10 or len(value) > 1000:
            raise ValueError("content must be between 10 and 1000 characters, inclusive")

        self._content = value

    def get_author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT authors.name FROM authors JOIN articles ON authors.id = articles.author_id WHERE articles.author_id = ? AND articles.magazine_id = ?', (self._author_id, self._magazine_id))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            raise ValueError("Article not found in the database")
        conn.close()
    
    def get_magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT magazines.name, magazines.category FROM magazines JOIN articles ON magazines.id = articles.magazine_id WHERE articles.author_id = ? AND articles.magazine_id = ?', (self._author_id, self._magazine_id))
        result = cursor.fetchone()
        if result:
            return Magazine(id=self.magazine_id, name=result[0], category=result[1])
        raise ValueError("Article not found in the database")
        conn.close()
    def __repr__(self):
        return f'<Article {self.title}>'

from database.connection import get_db_connection

class Author:
    def __init__(self, name):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string.")

        self._name = name

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?);", (self._name,))
        self._id = cursor.lastrowid
        connection.commit()
        connection.close()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Name must be a non-empty string.")
        self._name = value

    def articles(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
        SELECT title FROM articles WHERE author_id = ?;
        ''', (self._id,))
        articles = cursor.fetchall()
        connection.close()
        return [article[0] for article in articles]

    def magazines(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
        SELECT DISTINCT m.name FROM magazines m
        INNER JOIN articles a ON m.id = a.magazine_id
        WHERE a.author_id = ?;
        ''', (self._id,))
        magazines = cursor.fetchall()
        connection.close()
        return [magazine[0] for magazine in magazines]

    def __repr__(self):
        return f"Author(id={self._id}, name={self._name})"
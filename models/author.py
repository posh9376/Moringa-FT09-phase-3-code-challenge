from database.connection import get_db_connection


class Author:
    def __init__(self, id, name):
        self._id = id
        self._name = name
    @property #getter
    def id(self):
        return self._id

    @id.setter #setter
    def id(self, value):
        if not isinstance(value, int):
            raise TypeError("id must be an integer")
        self._id = value

    @property
    def name(self):
        if hasattr(self, '_name'):
            return self._name
        else:
            # Retrieve the name from the database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM authors WHERE id = ?', (self.id,))
            result = cursor.fetchone()
            if result:
                self._name = result[0]
            else:
                raise ValueError("Author not found in the database")
            conn.close()
            return self._name

    @name.setter
    def name(self, value):
        if hasattr(self, '_name'):
            raise AttributeError("name cannot be changed after author is instantiated")
        
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        if len(value) <= 0:
            raise ValueError("name must be longer than 0 characters")
        
        # Update the name in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE authors SET name = ? WHERE id = ?', (value, self.id))
        conn.commit()
        conn.close()
    
    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT articles.id, articles.title, articles.content, articles.created_at
            FROM articles
            JOIN authors ON articles.author_id = authors.id
            WHERE authors.id = ?
        ''', (self.id,))
        results = cursor.fetchall()
        conn.close()
        return [Article(id=result[0], title=result[1], content=result[2], created_at=result[3]) for result in results]
    
    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT magazines.id, magazines.name, magazines.category
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            JOIN authors ON articles.author_id = authors.id
            WHERE authors.id = ?
        ''', (self.id,))
        results = cursor.fetchall()
        conn.close()
        return [Magazine(id=result[0], name=result[1], category=result[2]) for result in results]

    def __repr__(self):
        return f'<Author {self.name}>'

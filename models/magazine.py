from database.connection import get_db_connection


class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self._name = name
        self._category = category

        # Create a new entry in the database magazines table
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (id, name, category) VALUES (?, ?, ?)', (self.id, self.name, self.category))
        conn.commit()
        conn.close()
    @property
    def id(self):
        return self._id

    @id.setter
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
            cursor.execute('SELECT name FROM magazines WHERE id = ?', (self.id,))
            result = cursor.fetchone()
            if result:
                self._name = result[0]
            else:
                raise ValueError("Magazine not found in the database")
            conn.close()
            return self._name
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        if len(value) < 2 or len(value) > 16:
            raise ValueError("name must be between 2 and 16 characters, inclusive")

        # Update the name in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE magazines SET name = ? WHERE id = ?', (value, self.id))
        conn.commit()
        conn.close()

        self._name = value

    @property
    def category(self):
        if hasattr(self, '_category'):
            return self._category
        else:
            # Retrieve the category from the database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT category FROM magazines WHERE id = ?', (self.id,))
            result = cursor.fetchone()
            if result:
                self._category = result[0]
            else:
                raise ValueError("Magazine not found in the database")
            conn.close()
            return self._category
    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise TypeError("category must be a string")
        if len(value) <= 0:
            raise ValueError("category must be longer than 0 characters")

        # Update the category in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE magazines SET category = ? WHERE id = ?', (value, self.id))
        conn.commit()
        conn.close()

        self._category = value
    
    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT articles.id, articles.title, articles.content, articles.created_at
            FROM articles
            JOIN magazines ON articles.magazine_id = magazines.id
            WHERE magazines.id = ?
        ''', (self.id,))
        results = cursor.fetchall()
        conn.close()
        return [Article(id=result[0], title=result[1], content=result[2], created_at=result[3]) for result in results]

    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.id, authors.name
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            JOIN magazines ON articles.magazine_id = magazines.id
            WHERE magazines.id = ?
        ''', (self.id,))
        results = cursor.fetchall()
        conn.close()
        return [Author(id=result[0], name=result[1]) for result in results]
    
    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT articles.title
            FROM articles
            JOIN magazines ON articles.magazine_id = magazines.id
            WHERE magazines.id = ?
        ''', (self.id,))
        results = cursor.fetchall()
        conn.close()
        return [result[0] for result in results] if results else None
    

    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.id, authors.name
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            JOIN magazines ON articles.magazine_id = magazines.id
            WHERE magazines.id = ?
            GROUP BY authors.id, authors.name
            HAVING COUNT(articles.id) > 2
        ''', (self.id,))
        results = cursor.fetchall()
        conn.close()
        if results:
            return [Author(id=result[0], name=result[1]) for result in results]
        else:
            return None
    def __repr__(self):
        return f'<Magazine {self.name}>'

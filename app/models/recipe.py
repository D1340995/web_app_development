from .db import get_db_connection

class Recipe:
    @staticmethod
    def create(title, description, ingredients, steps):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO recipes (title, description, ingredients, steps)
            VALUES (?, ?, ?, ?)
        ''', (title, description, ingredients, steps))
        conn.commit()
        recipe_id = cursor.lastrowid
        conn.close()
        return recipe_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        recipes = conn.execute('SELECT * FROM recipes ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(row) for row in recipes]

    @staticmethod
    def get_by_id(recipe_id):
        conn = get_db_connection()
        recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
        conn.close()
        return dict(recipe) if recipe else None

    @staticmethod
    def search(keyword):
        conn = get_db_connection()
        search_kw = f"%{keyword}%"
        recipes = conn.execute(
            'SELECT * FROM recipes WHERE title LIKE ? OR description LIKE ? ORDER BY created_at DESC', 
            (search_kw, search_kw)
        ).fetchall()
        conn.close()
        return [dict(row) for row in recipes]

    @staticmethod
    def update(recipe_id, title, description, ingredients, steps):
        conn = get_db_connection()
        conn.execute('''
            UPDATE recipes
            SET title = ?, description = ?, ingredients = ?, steps = ?
            WHERE id = ?
        ''', (title, description, ingredients, steps, recipe_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(recipe_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        conn.commit()
        conn.close()

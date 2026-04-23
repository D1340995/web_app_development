import sqlite3
from .db import get_db_connection

class User:
    @staticmethod
    def create(username):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
            conn.commit()
            user_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # username 已存在
            user_id = None
        conn.close()
        return user_id

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return dict(user) if user else None

class Collection:
    @staticmethod
    def add(user_id, recipe_id):
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO collections (user_id, recipe_id) VALUES (?, ?)', (user_id, recipe_id))
            conn.commit()
            success = True
        except sqlite3.IntegrityError:
            # 已經收藏過了，或是 user_id/recipe_id 不存在
            success = False
        conn.close()
        return success

    @staticmethod
    def remove(user_id, recipe_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM collections WHERE user_id = ? AND recipe_id = ?', (user_id, recipe_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_user_collections(user_id):
        conn = get_db_connection()
        recipes = conn.execute('''
            SELECT r.* FROM recipes r
            JOIN collections c ON r.id = c.recipe_id
            WHERE c.user_id = ?
            ORDER BY c.created_at DESC
        ''', (user_id,)).fetchall()
        conn.close()
        return [dict(row) for row in recipes]

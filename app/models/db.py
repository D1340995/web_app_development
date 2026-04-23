import sqlite3
import os

def get_db_connection():
    """
    建立並回傳與 SQLite 資料庫的連線。
    如果 instance 資料夾不存在會自動建立。
    """
    db_path = 'instance/database.db'
    db_dir = os.path.dirname(db_path)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
        
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    # 啟用 SQLite 外鍵約束支援
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

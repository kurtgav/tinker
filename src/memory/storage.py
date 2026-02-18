import sqlite3
import os

DB_PATH = os.path.expanduser("~/.tinker_memory.db")

class MemoryManager:
    _instance = None

    def __init__(self):
        self._init_db()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = MemoryManager()
        return cls._instance

    def _init_db(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_prefs (
                user_id TEXT,
                key TEXT,
                value TEXT,
                PRIMARY KEY (user_id, key)
            )
        """)
        conn.commit()
        conn.close()

    def set_pref(self, user_id: str, key: str, value: str):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO user_prefs (user_id, key, value)
            VALUES (?, ?, ?)
        """, (user_id, key, value))
        conn.commit()
        conn.close()

    def get_pref(self, user_id: str, key: str) -> str:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT value FROM user_prefs
            WHERE user_id = ? AND key = ?
        """, (user_id, key))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

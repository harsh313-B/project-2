import sqlite3

class Database:
    def __init__(self, db_name="game_data.db"):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.create_table()
        self.create_user_table()

    def create_table(self):
        """Creates a table to store game progress if it doesn't exist."""
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level INTEGER NOT NULL
            )
        """)
        self.conn.commit()

    def create_user_table(self):
        """Creates a table to store user data if it doesn't exist."""
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_user(self, username, password):
        """Adds a new user to the database."""
        self.cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()

    def check_user(self, username, password):
        """Checks if the user exists in the database."""
        self.cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return self.cur.fetchone() is not None

    def save_progress(self, level):
        """Saves the player's progress to the database."""
        self.cur.execute("INSERT INTO progress (level) VALUES (?)", (level,))
        self.conn.commit()

    def get_latest_level(self):
        """Gets the highest level the player has completed."""
        self.cur.execute("SELECT MAX(level) FROM progress")
        result = self.cur.fetchone()
        return result[0] if result[0] is not None else 1  # Default to level 1 if no progress

    def reset_progress(self):
        """Resets the progress (for restarting the game)."""
        self.cur.execute("DELETE FROM progress")
        self.conn.commit()

    def close(self):
        """Closes the database connection."""
        self.conn.close()

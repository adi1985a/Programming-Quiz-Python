import sqlite3
import hashlib
from database import create_database

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.achievements = []
        self.records = []

    def save_to_db(self):
        conn = create_database()
        c = conn.cursor()
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                  (self.username, self.email, self.password))
        conn.commit()
        conn.close()

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def register(username, email, password):
        conn = create_database()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? OR email=?", (username, email))
        if c.fetchone():
            conn.close()
            return False, "Username or email already exists."
        hashed = User.hash_password(password)
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed))
        conn.commit()
        conn.close()
        return True, "Registration successful."

    @staticmethod
    def login(username, password):
        conn = create_database()
        c = conn.cursor()
        hashed = User.hash_password(password)
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed))
        row = c.fetchone()
        conn.close()
        if row:
            return True, User(row[1], row[2], row[3])
        else:
            return False, "Invalid username or password."

    @staticmethod
    def get_user(username):
        conn = create_database()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        row = c.fetchone()
        conn.close()
        if row:
            return User(row[1], row[2], row[3])
        return None

    def get_achievements(self):
        conn = create_database()
        c = conn.cursor()
        c.execute("SELECT name, description, date FROM achievements WHERE user_id=(SELECT id FROM users WHERE username=?)", (self.username,))
        self.achievements = c.fetchall()
        conn.close()
        return self.achievements

    def get_records(self):
        conn = create_database()
        c = conn.cursor()
        c.execute("SELECT type, points, date FROM results WHERE user_id=(SELECT id FROM users WHERE username=?) ORDER BY points DESC", (self.username,))
        self.records = c.fetchall()
        conn.close()
        return self.records

    def has_achievement(self, name):
        conn = create_database()
        c = conn.cursor()
        c.execute("SELECT 1 FROM achievements WHERE user_id=(SELECT id FROM users WHERE username=?) AND name=?", (self.username, name))
        result = c.fetchone()
        conn.close()
        return result is not None

    def get_stats(self):
        conn = create_database()
        c = conn.cursor()
        c.execute("SELECT COUNT(*), MAX(points), AVG(points) FROM results WHERE user_id=(SELECT id FROM users WHERE username=?)", (self.username,))
        count, best, avg = c.fetchone()
        conn.close()
        return {'quizzes': count or 0, 'best': best or 0, 'avg': round(avg, 2) if avg else 0.0}

    @staticmethod
    def get_ranking():
        conn = create_database()
        c = conn.cursor()
        c.execute("SELECT u.username, SUM(r.points) as total FROM users u JOIN results r ON u.id = r.user_id GROUP BY u.username ORDER BY total DESC LIMIT 10")
        ranking = c.fetchall()
        conn.close()
        return ranking

    def grant_achievement(self, name, description):
        if not self.has_achievement(name):
            conn = create_database()
            c = conn.cursor()
            c.execute("INSERT INTO achievements (user_id, name, description, date) VALUES ((SELECT id FROM users WHERE username=?), ?, ?, datetime('now'))", (self.username, name, description))
            conn.commit()
            conn.close() 
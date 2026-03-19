import sqlite3
import os
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

class Authenticate:
    def __init__(self, db, folder):
        self.folder = folder
        self.db = db
        os.makedirs(folder, exist_ok=True)
        self.path = os.path.join(folder, db)
        self.conn = sqlite3.connect(self.path, timeout=5)
        self.c = self.conn.cursor()
        self.ph = PasswordHasher(
            time_cost=3,
            memory_cost=1000,
            parallelism=2,
            hash_len=32,
            salt_len=16
        )

    def create_user_folder(self, user_id):
        user_folder = os.path.join(self.folder, str(user_id))
        folders = [
            user_folder,
            os.path.join(user_folder, "lesson_images"),
            os.path.join(user_folder, "progress"),
            os.path.join(user_folder, "subjects")
        ]
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
        return user_folder

    def close(self):
        if self.conn:
            self.conn.close()

    def create_table(self):
        try:
            self.c.execute('''CREATE TABLE  users(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT UNIQUE,
                                name TEXT,
                                email TEXT UNIQUE,
                                password_hash TEXT NOT NULL,
                                learner_type TEXT
                        )''')
            
        except sqlite3.OperationalError:
            print(f"{self.db} already exists") 
        self.conn.commit()

    def insert_data(self, username="user123", name="Student 001", email="user123@gmail.com", password="12345678", learner_type="gamer"):
        try:
            password_hash = self.ph.hash(password=password)
            self.c.execute(
                'INSERT INTO users (username, name, email, password_hash, learner_type) VALUES (?, ?, ?, ?, ?)',
                (username, name, email, password_hash, learner_type)
            )
            self.conn.commit()
            user_id = self.c.lastrowid
            self.create_user_folder(user_id)
            print(f"Inserted data to users table and created folder for user {user_id}")
            return True
        except sqlite3.IntegrityError as e:
            print("Insert failed:", e)
            return False

    def verify_user(self, email, password):
        self.c.execute("SELECT id, password_hash FROM users WHERE email = ?", (email,))
        row = self.c.fetchone()

        if not row:
            return None

        user_id, stored_hash = row
        try:
            if self.ph.verify(stored_hash, password):
                self.create_user_folder(user_id)
                return user_id
            return None
        except VerifyMismatchError:
            return None

    


    def run(self):
        self.create_table()
        if self.verify_user(email="user123@gmail.com", password="12345678"):
            print("user exists, login Tick")

if __name__ == "__main__":
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)          
    print("Working directory set to:", os.getcwd())

    folder = "../data/user"
    db = "auth.db"

    auth = Authenticate(folder=folder, db=db)    

    auth.run()
    auth.insert_data(username="Diamond", name="Diamond Heart", email="d", password="d")

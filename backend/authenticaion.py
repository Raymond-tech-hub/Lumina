import sqlite3
import os
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

class Authenticate:
    def __init__(self, db, folder):
        self.folder = folder
        self.db = db
        self.path = os.path.join(folder, db)
        #self.conn = sqlite3.connect(self.path)
        self.conn = sqlite3.connect(self.path, timeout=5)
        self.c = self.conn.cursor() 
        self. ph = PasswordHasher(
            time_cost=3,
            memory_cost=1000,
            parallelism=2,
            hash_len=32,
            salt_len=16
        )

    def close(self):
        if self.conn:
            self.conn.close()

    def create_table(self):
        try:
            self.c.execute('''CREATE TABLE  users(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT UINIQUE,
                                name TEXT,
                                email TEXT UNIQUE,
                                password_hash TEXT NOT NULL,
                                learner_type TEXT DEFAULT 'gamer'
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
            print("Inserted data to users table")
            return True
        except sqlite3.IntegrityError as e:
            print("Insert failed:", e) 
            return False

    def verify_user(self, email, password):
        self.c.execute("SELECT id, password_hash FROM users WHERE email = ?", (email,))
        row = self.c.fetchone()
        
        if not row:
            return None  # No user found
        
        user_id, stored_hash = row

        try:
            if self.ph.verify(stored_hash, password):
                return user_id  # Return actual user id
            else:
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
    auth.insert_data(username="Diamond", name="Diamond Heart", email="d", password="1")

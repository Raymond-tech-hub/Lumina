import os
import json
from kivymd.uix.screen import MDScreen
from backend.authenticaion import Authenticate
from kivymd.app import MDApp
from backend.user_builder import UserBuilder
from kivy.clock import Clock
from kivy.animation import Animation


class PathSelection(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.learning_path = "gamer" #default

    def try_signup(self):
        app = MDApp.get_running_app()

        # --- Step 1: Get data stored from SignupScreen ---
        signup_data = getattr(app, "temp_signup_data", None)
        if not signup_data:
            print("No signup data found.")
            return

        username = signup_data["username"]
        full_name = signup_data["name"]
        email = signup_data["email"]
        password = signup_data["password"]

        try:
            # --- Step 2: Insert into authentication DB ---
            folder = "data/user"
            database_file = "auth.db"
            self.auth = Authenticate(folder=folder, db=database_file)

            success = self.auth.insert_data(
                username=username,
                name=full_name,
                email=email,
                password=password,
                learner_type=self.learning_path 
            )

            if not success:
                self.auth.c.execute("SELECT 1 FROM users WHERE username = ?", (username,))
                if self.auth.c.fetchone():
                    print("Username already exists")

                self.auth.c.execute("SELECT 1 FROM users WHERE email = ?", (email,))
                if self.auth.c.fetchone():
                    print("Email already exists")
                return

            print("User registered successfully!")

            # --- Step 3: Get user_id ---
            self.auth.c.execute("SELECT id FROM users WHERE email = ?", (email,))
            self.row = self.auth.c.fetchone()

            if not self.row:
                print("Error: user ID not found after insertion")
                return
            
            user_id = self.row[0]

            # --- Step 4: Build folder structure ---
            builder = UserBuilder(
                base_path="data/user",
                learner_type=self.learning_path 
            )
            builder.build_user(user_id)

            print(f"Folder structure created for user ID {user_id}")

            # --- Step 5: Load user and go home ---
            app.load_user_graphs(user_id)
            self.manager.current = "home"

        except Exception as e:
            print("error in sign up:", e)

        finally:
            if hasattr(self, "auth"):
                self.auth.close()

class SignupScreen(MDScreen):
    def on_enter(self):
        print("Signup screen entered")

    def switch_to_login(self):
        self.manager.current = "login"

    def go_path_selection(self):
        username = self.ids.username_field.text.strip()
        full_name = self.ids.name_field.text.strip()
        email = self.ids.email_field.text.strip()
        password = self.ids.password_field.text.strip()
        confirm_password = self.ids.confirm_password.text.strip()

        if not all([username, full_name, email, password, confirm_password]):
            print("All fields required")
            return

        if password != confirm_password:
            print("Passwords do not match")
            return

        # Store temporarily in App memory
        app = MDApp.get_running_app()
        app.temp_signup_data = {
            "username": username,
            "name": full_name,
            "email": email,
            "password": password
        }

        self.manager.current = "path_selection"
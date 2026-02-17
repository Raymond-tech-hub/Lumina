#frontend/scripts/LoginScreen.py

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from backend.authenticaion import Authenticate
import re
import os

class LoginScreen(MDScreen):
    def on_enter(self):
        print("Login screen entered")

    def try_login(self):
        email = self.ids.email_field.text.strip()
        password = self.ids.password_field.text.strip()
        folder = "data/user"
        database_file = "auth.db" 

        auth = Authenticate(folder=folder, db=database_file)
        print("Login attempt initiated")

        user_id = auth.verify_user(email, password)
        if user_id :
            print("Login successful!")
            # Set the app's current user
            app = MDApp.get_running_app()
            app.load_user_graphs(user_id)  # loads graphs & sets current_user
            self.manager.current = "home"
        else:
            self.ids.password_field.error = True
            self.ids.password_field.helper_text = "Incorrect email or password"
            print("Login failed")



    def switch_to_signup(self):
        self.manager.current = "signup"

    def validate_email(self, email):
        pattern = r'[\w.-]+@[\w.-]+\.\w+'
        is_valid = re.match(pattern, email) is not None
        print(f"Email validation for '{email}': {is_valid}")
        return is_valid
    
    def validate_password(self, password):
        length = len(password)
        character_types = sum(bool(re.search(pattern, password)) for pattern in [r'[A-Z]', r'[a-z]', r'[0-9]', r'[\W_]'])
        is_valid = length >= 6 and character_types >= 2
        print(f"Password validation: {is_valid}")
        return {
            "is_valid": is_valid,
            "length": length,
            "character_types": character_types
        }
    
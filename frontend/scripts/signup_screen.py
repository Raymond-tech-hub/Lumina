import os
import json
from kivymd.uix.screen import MDScreen
from backend.authenticaion import Authenticate
from kivymd.app import MDApp
from backend.user_builder import UserBuilder
from kivy.clock import Clock
from kivy.animation import Animation


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

        app = MDApp.get_running_app()
        app.switch_to("path_selection")
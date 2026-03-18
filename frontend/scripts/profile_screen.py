import os
import json
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.animation import Animation
from kivymd.app import MDApp
from backend.authenticaion import Authenticate

class ProfileScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.folder = "data/user"
        self.db = "auth.db"
        self.auth = Authenticate(folder=self.folder, db=self.db)

    def on_enter(self, *args):
        print("Home screen entered")
        # Logo pulse once when entering the screen
        Clock.schedule_once(self._pulse_logo, 0.8)
        self.load_info()

    def _pulse_logo(self, dt):
        logo = self.ids.get('logo')
        if logo:
            anim = (Animation(opacity=0.45, duration=1.0, t='out_quad') +
                    Animation(opacity=1.0, duration=1.0, t='out_quad'))
            anim.repeat = True
            anim.start(logo)

    def load_info(self):
        app = MDApp.get_running_app()
        user_id = getattr(app, "current_user", None)

        if not user_id:
            print("No user logged in.")
            return

        try:
            self.auth.c.execute(
                "SELECT username, name, email, learner_type FROM users WHERE id = ?",
                (user_id,)
            )
            row = self.auth.c.fetchone()
            self.auth.close()

            if not row:
                print("User not found in database.")
                return

            username, full_name, email, learner_type = row

            # -------- Update UI --------
            self.ids.username_label.text = f"Username: {username}"
            self.ids.fullname_label.text = f"Full Name: {full_name}"
            self.ids.email_label.text = f"Email: {email}"
            self.ids.learner_type_label.text = f"Learning Style: {learner_type}"

        except Exception as e:
            print("Error loading profile:", e)

    def go_home(self):
        self.manager.current = "home"

    def go_profile(self):
        print("entering profile")
        self.manager.current = "profile"

    def go_tasks(self):
        print("entering tasks")
        self.manager.current = "tasks"

    def go_quiz(self):
        print("entering quiz")
        self.manager.current = "quiz"

    def go_leaderboard(self):
        print("entering leaderboard")
        self.manager.current = "leaderboard"
"""
Loading screen helper.
Loads KV files in a background thread to avoid blocking the UI, then
switches to the 'login' screen on the main thread when done.

"""


from ast import Load
import os

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.clock import Clock, mainthread

import threading

PRIMARY_KV = [
    "frontend/screens/login.kv",
    "frontend/screens/signup.kv",
    "frontend/screens/home.kv"
]

SECONDARY_KV = [
    "frontend/screens/lesson.kv",
    "frontend/screens/quiz.kv",
    "frontend/screens/tasks.kv",
    "frontend/screens/profile.kv",
    "frontend/screens/tutor.kv",
    "frontend/screens/lesson_progress.kv",
    "frontend/screens/mini_quest.kv",
    "frontend/screens/timetable.kv"
]

class LoadingScreen(MDScreen):
    """Screen that loads KV files in background, then navigates to login."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dot_state = 0

    def on_enter(self):
        self.dot_state = 0
        self.is_loaded = False
        self.ids.loading_slider.value = 0
        Clock.schedule_interval(self.animate_dots, 0.25)

        self.image_path = "frontend/assets/loading/loading_image.jpg"

        # To DO: Not good, change this part
        thread = threading.Thread(target=self.heavy_load, daemon=True)
        thread.start()

    def animate_dots(self, dt):
        # Update loading dots
        self.dot_state = (self.dot_state + 1) % 4
        self.ids.loading_text.text = "Loading" + "." * self.dot_state

        slider = self.ids.loading_slider
        if slider.value < slider.max:
            slider.value = min(slider.max, slider.value + 8)

        if self.is_loaded and slider.value >= slider.max:
            Clock.unschedule(self.animate_dots)
            self._go_to_login(0)

    def heavy_load(self):
        """Background task: validate assets and prepare KV files."""
        self.validate_assets()
        Clock.schedule_once(lambda dt: self.load_kv_mainthread())

    @mainthread
    def laod_kv_background(self, kv_files):
        """Load KV files in a background thread."""
        for kv in kv_files:
            try:
                Builder.load_file(kv)
                print(f"Loaded KV: {kv}")
            except Exception as e:
                print(f"Failed to load KV {kv}: {e}")

    def load_kv_mainthread(self):
        """Load KV files on the main thread to avoid Kivy threading issues."""
        #Load primary KV files first to ensure login screen is ready
        self.laod_kv_background(PRIMARY_KV)

        #load secondary KV files in the background while user is on login screen
        threading.Thread(target=self.laod_kv_background, args=(SECONDARY_KV,), daemon=True).start()

        self.is_loaded = True

    def validate_assets(self):
        # Check if all assets in config exist
        app = MDApp.get_running_app()
        config = app.config
        missing_assets = []
        for name, path in config.get("Assets", {}).items():
            if not os.path.exists(path):
                print(f"[MISSING] {name} → {path}")
                missing_assets.append(f"{name} → {path}")   

        if missing_assets:
            print("Missing assets:")
            for asset in missing_assets:
                print(f" - {asset}")
        else:
            print("All assets validated successfully.")

    def asset_exists(self, asset_path):
        # Check if asset exists in the filesystem
        try:
            with open(asset_path, "r"):
                return True
        except FileNotFoundError:
            return False
        
    @mainthread
    def _go_to_login(self, dt):
        if not self.manager.has_screen("login"):
            from frontend.scripts.login_screen import LoginScreen
            self.manager.add_widget(LoginScreen(name="login"))

        self.manager.current = "login"
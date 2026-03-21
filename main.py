#Main.py

import os
import json

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)          
print("Working directory set to:", os.getcwd())

from kivymd.app import MDApp
from kivymd.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import FadeTransition
from kivy.lang import Builder
from kivy.uix.image import AsyncImage
from kivy.uix.behaviors import ButtonBehavior

# Import only loading screen initially to show UI quickly
from frontend.scripts.loading_screen import LoadingScreen

class LuminaScreenManager(ScreenManager):
    pass

class LuminaApp(MDApp):
    def __init__(self, default_user_id=None, **kwargs):
        super().__init__(**kwargs)
        self.default_user_id = default_user_id
        self.current_user = None

    def build(self):
        # 1. Load config
        self.load_config()

        # 2. Assign assets globally for KV
        for name, path in self.config.get("Assets", {}).items():
            setattr(self, name, path)

        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = 'Dark'

        sm = LuminaScreenManager(transition=FadeTransition(duration=0.8))

        self.loading_kivy_path = "frontend/screens/loading.kv"
        try:
            if os.path.exists(self.loading_kivy_path):
                Builder.load_file(self.loading_kivy_path)
                print("Successfully loaded loading.kv")
            else:
                print(f"loading.kv does not exist: {self.loading_kivy_path}")
        except Exception as e:
            print("Error loading 'loading.kv':", e)

        sm.add_widget(LoadingScreen(name="loading"))
        sm.current = "loading"
        return sm

    def load_config(self):
        config_path = "frontend/config/ConfigFile.json"
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file missing: {config_path}")

        with open(config_path, "r") as f:
            self.config = json.load(f)

        print("Config loaded successfully.")

class ImageButton(ButtonBehavior, AsyncImage):
    pass

if __name__ == "__main__":
    app = LuminaApp(default_user_id=1)
    app.run()

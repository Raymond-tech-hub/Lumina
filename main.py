import os
import json
from kivymd.app import MDApp
from kivymd.uix.screenmanager import ScreenManager
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import AsyncImage
from kivy.lang import Builder

PRIMARY_KV = [
    "frontend/screens/loading.kv",
    "frontend/screens/login.kv",
    "frontend/screens/signup.kv",
    "frontend/screens/home.kv"
]

class LuminaApp(MDApp):
    def __init__(self, default_user_id=None, **kwargs):
        super().__init__(**kwargs)
        self.default_user_id = default_user_id
        self.current_user = None
        self.config = {}           # Will hold config.json
        self.cached_screens = {}   # Screen cache
        self.screen_manager = None

    def build(self):
        # Theme
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"

        # Load config
        self.load_config()
        self.assign_assets()

        # Load primary KV files
        for kv in PRIMARY_KV:
            Builder.load_file(kv)

        # Setup ScreenManager
        from kivy.uix.screenmanager import FadeTransition
        self.screen_manager = ScreenManager(transition=FadeTransition())

        # Load first screen manually
        self.add_screen("loading")
        self.screen_manager.current = "loading"
        return self.screen_manager

    def load_config(self):
        config_path = "frontend/config/ConfigFile.json"
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
        print("[CONFIG LOADED]")

    def assign_assets(self):
        """Map each asset in config as an app attribute for KV access."""
        assets = self.config.get("Assets", {})
        for key, path in assets.items():
            setattr(self, key, path)  # e.g., app.app_logo2
        print("[ASSETS ASSIGNED]")

    def add_screen(self, screen_name):
        """Add screen to manager if not cached."""
        if screen_name in self.cached_screens:
            return self.cached_screens[screen_name]

        # Dynamic import
        mod_name = f"frontend.scripts.{screen_name.lower()}_screen"
        mod = __import__(mod_name, fromlist=[screen_name.capitalize() + "Screen"])
        cls = getattr(mod, screen_name.capitalize() + "Screen")
        screen = cls(name=screen_name)

        self.cached_screens[screen_name] = screen
        self.screen_manager.add_widget(screen)
        return screen

    def switch_to(self, screen_name):
        """Switch screens using cache."""
        self.add_screen(screen_name)
        self.screen_manager.current = screen_name


class ImageButton(ButtonBehavior, AsyncImage):
    """Clickable image for KV use."""
    pass


if __name__ == "__main__":
    # Ensure working directory is script location
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("Working directory:", os.getcwd())
    LuminaApp(default_user_id=1).run()
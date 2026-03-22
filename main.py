import os

'''abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)          
print("Working directory set to:", os.getcwd())'''

import json
import importlib

from kivymd.app import MDApp
from kivymd.uix.screenmanager import ScreenManager
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import AsyncImage
from kivy.lang import Builder

PRIMARY_KV = [
    "frontend/screens/loading.kv",
    "frontend/screens/login.kv",
    "frontend/screens/signup.kv",
    "frontend/screens/home.kv",
    "frontend/screens/tutor.kv"
]

class LuminaApp(MDApp):
    def __init__(self, default_user_id=None, **kwargs):
        super().__init__(**kwargs)
        self.default_user_id = default_user_id
        self.current_user = None
        self.config = {}           # Will hold config.json
        self.cached_screens = {}   # Screen cache
        self.screen_manager = None
        self.graphs = []
        self.current_id = 0
        self.current_graph = None

    def lazy_load_screen(self, screen_name):
        """Load any other screen lazily."""
        app = MDApp.get_running_app()
        if screen_name in app.cached_screens:
            return app.cached_screens[screen_name]

        mod_name = f"frontend.scripts.{screen_name.lower()}_screen"
        mod = importlib.import_module(mod_name)
        class_name = "".join([word.capitalize() for word in screen_name.split("_")]) + "Screen"
        cls = getattr(mod, class_name)
        screen = cls(name=screen_name)
        app.cached_screens[screen_name] = screen
        if app.screen_manager:
            app.screen_manager.add_widget(screen)
        return screen

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

    def load_user_graphs(self, user_id):
        self.current_user = str(user_id)  # store current user
        user_folder = os.path.join("data/user", self.current_user)

        if not os.path.exists(user_folder):
            print(f"No folder for user {self.current_user}")
            self.graphs = []
            self.current_graph = None
            return

        self.graphs = [f for f in os.listdir(user_folder) if f.lower().endswith(".png")]
        self.current_id = 0

        if self.graphs:
            self.current_graph = os.path.join(user_folder, self.graphs[0])
            # Update home screen if loaded
            try:
                home_screen = self.screen_manager.get_screen("home")
                home_screen.ids.graph_image.source = self.current_graph
                home_screen.ids.graph_image.reload()
            except Exception as e:
                print("Home screen not ready yet:", e)
        else:
            self.current_graph = None

        print(f"User {self.current_user} graphs loaded: {self.graphs}")

    def graph_back(self):
        if self.current_id > 0:
            self.current_id -= 1
            self.update_graph_image()

    def graph_forward(self):
        if self.current_id < len(self.graphs) - 1:
            self.current_id += 1
            self.update_graph_image()

    def update_graph_image(self):
        if not self.graphs:
            print("No graphs to display")
            return

        home_screen = self.screen_manager.get_screen("home")
        home_screen.ids.graph_image.source = os.path.join(
            "data/user", self.current_user, self.graphs[self.current_id]
        )
        home_screen.ids.graph_image.reload()


class ImageButton(ButtonBehavior, AsyncImage):
    """Clickable image for KV use."""
    pass


if __name__ == "__main__":
    # Ensure working directory is script location
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("Working directory:", os.getcwd())
    LuminaApp(default_user_id=1).run()
import os
import threading
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.clock import Clock, mainthread

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dot_state = 0
        self.is_loaded = False

    def on_enter(self):
        self.ids.loading_slider.value = 0
        Clock.schedule_interval(self.animate_dots, 0.25)
        threading.Thread(target=self.heavy_load, daemon=True).start()

    def animate_dots(self, dt):
        self.dot_state = (self.dot_state + 1) % 4
        self.ids.loading_text.text = "Loading" + "." * self.dot_state
        slider = self.ids.loading_slider
        if slider.value < slider.max:
            slider.value = min(slider.max, slider.value + 8)
        if self.is_loaded and slider.value >= slider.max:
            Clock.unschedule(self.animate_dots)
            self._go_to_login(0)

    def heavy_load(self):
        """Validate assets and prepare KV files."""
        self.validate_assets()
        Clock.schedule_once(lambda dt: self.load_primary_kv())

    @mainthread
    def load_primary_kv(self):
        """Load primary KV files on main thread."""
        for kv in PRIMARY_KV:
            if os.path.exists(kv):
                try:
                    Builder.load_file(kv)
                    print(f"[LOADED] {kv}")
                except Exception as e:
                    print(f"[ERROR] Failed to load KV {kv}: {e}")
            else:
                print(f"[MISSING] KV file not found: {kv}")

        # Load secondary KV files in background
        threading.Thread(target=self.load_secondary_kv, daemon=True).start()

        # Prepare cached screens
        app = MDApp.get_running_app()
        if not hasattr(app, "cached_screens"):
            app.cached_screens = {}

        self.is_loaded = True

    def load_secondary_kv(self):
        """Lazy-load secondary KV files."""
        for kv in SECONDARY_KV:
            if os.path.exists(kv):
                try:
                    Builder.load_file(kv)
                    print(f"[LOADED] {kv}")
                except Exception as e:
                    print(f"[ERROR] Failed to load KV {kv}: {e}")
            else:
                print(f"[MISSING] KV file not found: {kv}")

    def validate_assets(self):
        """Ensure all assets exist before app start."""
        app = MDApp.get_running_app()
        if not hasattr(app, "config"):
            print("[WARNING] App config not loaded yet. Skipping asset check.")
            return

        missing_assets = []
        for name, path in app.config.get("Assets", {}).items():
            if not os.path.exists(path):
                missing_assets.append(f"{name} → {path}")

        if missing_assets:
            print("[MISSING ASSETS]:")
            for asset in missing_assets:
                print(f" - {asset}")
        else:
            print("[ASSETS VALID] All assets exist.")

    @mainthread
    def _go_to_login(self, dt):
        if not self.manager.has_screen("login"):
            from frontend.scripts.login_screen import LoginScreen
            self.manager.add_widget(LoginScreen(name="login"))
        self.manager.current = "login"
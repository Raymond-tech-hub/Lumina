import os
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.core.audio import SoundLoader

SECONDARY_KV = [
    "frontend/screens/lesson.kv",
    "frontend/screens/quiz.kv",
    "frontend/screens/tasks.kv",
    "frontend/screens/profile.kv",
    "frontend/screens/lesson_progress.kv",
    "frontend/screens/mini_quest.kv",
    "frontend/screens/timetable.kv",
    "frontend/screens/path_selection.kv"
]

class LoadingScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dot_state = 0
        # Track slider progress
        self.completed_tasks = 0
        self.total_tasks = len(SECONDARY_KV) + 2  # +2 for asset validation and tutor screen
        self.is_loaded = False

    def on_enter(self):
        self.ids.loading_slider.value = 0
        Clock.schedule_interval(self.animate_dots, 0.25)
        Clock.schedule_once(lambda dt: self.start_loading(), 0)

    def animate_dots(self, dt):
        self.dot_state = (self.dot_state + 1) % 4
        self.ids.loading_text.text = "Loading" + "." * self.dot_state

        # Update slider based on tasks completed
        slider = self.ids.loading_slider
        slider.value = (self.completed_tasks / self.total_tasks) * slider.max

        if self.completed_tasks >= self.total_tasks:
            Clock.unschedule(self.animate_dots)
            self._go_to_login(0)

    def start_loading(self):
        """Load assets and KV files sequentially on main thread."""

        # Validate assets first
        self.validate_assets()
        self.completed_tasks += 1

        # Start Background music loading in a separate thread
        self.load_background_music()

        for kv in SECONDARY_KV:
            if os.path.exists(kv):
                try:
                    Builder.load_file(kv)
                    print(f"[LOADED] {kv}")
                except Exception as e:
                    print(f"[ERROR] Failed to load KV {kv}: {e}")
            else:
                print(f"[MISSING] KV file not found: {kv}")
            self.completed_tasks += 1

        app = MDApp.get_running_app()
        if not hasattr(app, "cached_screens"):
            app.cached_screens = {}

        # Load Tutor screen (heavy asset) last
        self.load_tutor_screen()

    def load_tutor_screen(self):
        """Eagerly import heavy tutor screen and update progress."""
        from frontend.scripts.tutor_screen import TutorScreen

        app = MDApp.get_running_app()
        tutor = TutorScreen(name="tutor")
        app.cached_screens["tutor"] = tutor
        if app.screen_manager:
            app.screen_manager.add_widget(tutor)

        # Increment slider to account for this heavy screen
        self.completed_tasks += 1

    def load_background_music(self):
        """Load and play background music."""
        try:
            app = MDApp.get_running_app()
            if not hasattr(app, "config") or "Sounds" not in app.config:
                print("[AUDIO] No Sounds config found.")
                self.completed_tasks += 1
                return

            # Pick a theme (for example, theme1)
            music_path = app.config["Sounds"].get("theme2")
            if not music_path or not os.path.exists(music_path):
                print(f"[AUDIO] Background music file not found: {music_path}")
                self.completed_tasks += 1
                return

            self.background_music = SoundLoader.load(music_path)
            if self.background_music:
                self.background_music.loop = True
                self.background_music.play()
                print(f"[AUDIO] Playing background music: {music_path}")
            else:
                print("[AUDIO] Failed to load music.")
        except Exception as e:
            print(f"[AUDIO ERROR] {e}")
        finally:
            self.completed_tasks += 1

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
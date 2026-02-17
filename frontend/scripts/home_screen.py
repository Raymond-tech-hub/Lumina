from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.animation import Animation
from kivymd.app import MDApp
from kivy.properties import StringProperty

from backend.tree import Tree

class HomeScreen(MDScreen):
    tree_image_source = StringProperty("data/user/seedling.jpeg")
    coins_text = StringProperty("Coins: 0")
    xp_text = StringProperty("XP: 0")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_tree = None

    def on_enter(self, *args):
        print("entered home screen")
        app = MDApp.get_running_app()
        self.current_user = app.current_user

        # Initialize user's tree
        self.user_tree = Tree(self.current_user)

        # Update variables for KV
        self.tree_image_source = self.user_tree.ui_data["current_image"]
        self.coins_text = f"Coins: {self.user_tree.ui_data['coins']}"
        self.xp_text = f"XP: {self.user_tree.ui_data['xp']}"

        print(self.user_tree)
        print(self.tree_image_source)
        print(self.xp_text, self.coins_text)

        # Pulse the logo
        Clock.schedule_once(self._pulse_logo, 0.8)

    def update_tree_ui(self):
        """Update tree image, XP, and coins in the UI."""
        progress = self.user_tree.get_progress()
        
        # Update tree image
        tree_image_widget = self.ids.tree_image
        tree_image_widget.source = progress["current_image"]
        
        # Update XP and Coins labels
        self.ids.xp_label.text = f"XP: {progress['xp']}"
        self.ids.coins_label.text = f"Coins: {progress['coins']}"

    def toggle_menu_panel(self):
        panel = self.ids.menu_slider_panel
        bg = self.ids.slider_bg

        if panel.disabled:
            # Enable panel and background
            panel.disabled = False
            bg.disabled = False
            Animation(opacity=1, d=0.25).start(bg)

            # Start panel off-screen left
            panel.pos_hint = {"x": -0.7, "y": 0.05}  # start left
            Animation(pos_hint={"x": 0, "y": 0.05}, opacity=0.95, d=0.25, t='out_quad').start(panel)

        else:
            # Hide panel
            anim = Animation(pos_hint={"x": -0.7, "y": 0.05}, opacity=0, d=0.25, t='in_quad')
            anim.bind(on_complete=lambda *args: self._hide_menu_panel())
            anim.start(panel)
            Animation(opacity=0, d=0.25).start(bg)

    def _hide_menu_panel(self):
        self.ids.menu_slider_panel.disabled = True
        self.ids.slider_bg.disabled = True

    def hide_menu_panel(self, *args):
        if not self.ids.menu_slider_panel.disabled:
            self.toggle_menu_panel()

    def _pulse_logo(self, dt):
        logo = self.ids.get('logo')
        if logo:
            anim = (Animation(opacity=0.45, duration=1.0, t='out_quad') +
                    Animation(opacity=1.0, duration=1.0, t='out_quad'))
            anim.repeat = True
            anim.start(logo)

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

    def go_tutor(self):
        print("entering tutor")
        self.manager.current = "tutor"

    def go_lesson(self):
        print("entering lesson")
        self.manager.current = "lesson"

'''def start_logo_pulse(self, dt):
        logo = self.ids.logo
        if logo:
            # Create pulse animation (scale up + down)
            anim = (Animation(opacity=0.5, duration=0.8) +
                    Animation(opacity=1.0, duration=0.8))
            anim.repeat = True  # repeat indefinitely
            anim.start(logo)'''

    
    

    
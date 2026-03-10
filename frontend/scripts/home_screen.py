from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.animation import Animation
from kivymd.app import MDApp
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
import time

from backend.tree import Tree

class HomeScreen(MDScreen):
    tree_image_source = StringProperty("data/user/seedling.jpeg")
    coins_text = StringProperty("Coins: 0")
    xp_text = StringProperty("XP: 0")

    timer_limit = 0
    timer_text = StringProperty("00:00")
    seconds_left = NumericProperty(0)
    timer_running = BooleanProperty(False)
    timer_event = None

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

        #open timer dialogbox
        if self.timer_limit == 0:
            Clock.schedule_once(lambda dt: self.show_popup(), 0.5)
            self.timer_limit += 1

    def start_timer(self, minutes):
        if self.timer_running:
            return

        self.seconds_left = minutes * 60
        self.timer_running = True

        minutes_display = self.seconds_left // 60
        seconds_display = self.seconds_left % 60
        self.timer_text = f"{minutes_display:02}:{seconds_display:02}"

        self.dialog.dismiss()

        self.timer_event = Clock.schedule_interval(self._update_timer, 1)

    def stop_timer(self):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_running = False

    def show_popup(self):
        if hasattr(self, "dialog") and self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            title="Start Study Session",
            text="Choose your study duration:",
            buttons=[
                MDRaisedButton(
                    text="5 min",
                    on_release=lambda x: self.start_timer(5)
                ),
                MDRaisedButton(
                    text="20 min",
                    on_release=lambda x: self.start_timer(20)
                ),
                MDRaisedButton(
                    text="45 min",
                    on_release=lambda x: self.start_timer(45)
                ),
            ],
        )
        self.dialog.open()

    def _update_timer(self, dt):
        if self.seconds_left <= 0:
            self.finish_session()
            return

        self.seconds_left -= 1

        minutes = self.seconds_left // 60
        seconds = self.seconds_left % 60

        self.timer_text = f"{minutes:02}:{seconds:02}"

    def finish_session(self):
        if self.timer_event:
            self.timer_event.cancel()

        self.timer_running = False

        # reward user
        self.user_tree.add_xp(20)
        self.user_tree.add_coins(5)

        self.update_tree_ui()

        dialog = MDDialog(
            title="Session Complete 🎉",
            text="Great job! Your tree has grown.",
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

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

    def go_login(self):
        print("entering login")
        self.manager.current = "login"

'''def start_logo_pulse(self, dt):
        logo = self.ids.logo
        if logo:
            # Create pulse animation (scale up + down)
            anim = (Animation(opacity=0.5, duration=0.8) +
                    Animation(opacity=1.0, duration=0.8))
            anim.repeat = True  # repeat indefinitely
            anim.start(logo)'''

    
    

    
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.animation import Animation

class ProfileScreen(MDScreen):
    def on_enter(self, *args):
        print("Home screen entered")
        # Logo pulse once when entering the screen
        Clock.schedule_once(self._pulse_logo, 0.8)

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
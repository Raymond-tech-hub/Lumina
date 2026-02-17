from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.animation import Animation

class HomeScreen(MDScreen):
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

    
    

    
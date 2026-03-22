# base_game.py

from turtle import width

from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window

from scripts.animate_player import AnimatedPlayer 


class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # =========================
        # BACKGROUND (FULL SCREEN)
        # =========================
        self.bg = Image(
            source="assets/images/mid_cell_background.jpeg",  # <-- replace
            allow_stretch=True,
            keep_ratio=False,
            size=Window.size,
            pos=(0, 0)
        )
        self.add_widget(self.bg)

        # =========================
        # TERRAIN (BOTTOM STRIP)
        # =========================
        self.terrain = Image(
            source="assets/images/grass_terrain_3.jpeg",  # <-- replace
            size_hint=(1, None),
            height=120,
            width=Window.width,
            pos=(0, 0)
        )
        self.add_widget(self.terrain)

        # =========================
        # PLAYER
        # =========================
        self.player = AnimatedPlayer(
            size=(80, 80),
            pos=(100, 120)
        )
        self.add_widget(self.player)

        # Movement variables
        self.velocity_x = 0
        self.speed = 5

        # Start game loop
        Clock.schedule_interval(self.update, 1 / 60)

        # Input
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)

    # =========================
    # INPUT HANDLING
    # =========================
    def on_key_down(self, window, key, scancode, codepoint, modifier):
        if key == 276:  # LEFT
            self.velocity_x = -self.speed
        elif key == 275:  # RIGHT
            self.velocity_x = self.speed

    def on_key_up(self, window, key, scancode):
        if key in (276, 275):
            self.velocity_x = 0

    # =========================
    # GAME LOOP
    # =========================
    def update(self, dt):
        # Move player
        self.player.x += self.velocity_x

        # Simple boundary clamp
        if self.player.x < 0:
            self.player.x = 0
        if self.player.right > Window.width:
            self.player.right = Window.width


# =========================
# APP ROOT
# =========================
class GameApp(MDApp):
    def build(self):
        return GameWidget()


if __name__ == "__main__":
    GameApp().run()
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image

class AnimatedPlayer(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Load full spritesheet
        self.sheet = CoreImage("assets/characters/3 Cyborg/Cyborg_idle.png").texture

        print(self.sheet.width, self.sheet.height)

        # Rows and Columns
        self.row = 4
        self.column = 1

        # Calculate frame width
        self.frame_width = self.sheet.width // self.column
        self.frame_height = self.sheet.height // self.row

        # Store frames
        self.frames = []

        for i in range(self.column):
            frame = self.sheet.get_region(
                i * self.frame_width,  # x
                0,                     # y
                self.frame_width,
                self.frame_height
            )
            self.frames.append(frame)

        # Set first frame
        self.frame_index = 0
        self.texture = self.frames[0]

        # Animation speed
        from kivy.clock import Clock
        Clock.schedule_interval(self.animate, 0.15)

    def animate(self, dt):
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.texture = self.frames[self.frame_index]
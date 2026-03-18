from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.lang import Builder
from voice import Voice
from kivy.properties import NumericProperty
from kivy.animation import Animation

from threading import Thread
import os

# Load KV first
kv_path = os.path.join(os.path.dirname(__file__), "voicekvfile.kv")
if os.path.exists(kv_path):
    Builder.load_file(kv_path)
else:
    print("KV file does not exist!")


# --- Screen class ---
class VoiceChatScreen(MDScreen):
    circle_size = NumericProperty(300)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.voice = Voice()  # initialize TTS
        

    def say_hello(self):
        text = "Hello this is a voice chat from Lumina your AI tutor!, how may i be of assistant?"

        self.animate_circle()

        def speak_thread():
            self.voice.speak(text)
            # Stop animation when done
            # Reset circle size
            Animation.cancel_all(self, 'circle_size')
            self.circle_size = 300

        Thread(target=speak_thread, daemon=True).start()

    def animate_circle(self):
        # This creates a pulsing animation
        anim = Animation(circle_size=270, duration=0.5) + Animation(circle_size=290, duration=0.4)
        anim.repeat = True
        anim.start(self)  # animate the root's circle_size


# --- App class ---
class VoiceChatApp(MDApp):
    def build(self):
        return VoiceChatScreen()  # return the screen

if __name__ == "__main__":
    VoiceChatApp().run()

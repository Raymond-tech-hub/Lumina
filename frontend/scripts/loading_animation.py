from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.clock import Clock
import os

# Optional: set a nice window size for testing
Window.size = (400, 700)  # phone-like

class LoadingAnimation(MDScreen):
    def on_enter(self):
        """Bind to video player and wait for video to finish before switching to loading."""
        print("LoadingAnimation entered")
        
        # Get the absolute path to the video file
        video_path = os.path.join(os.path.dirname(__file__), "..", "screens", "anim.mp4")
        video_path = os.path.abspath(video_path)
        print(f"Video path: {video_path}")
        
        try:
            # Get the video player from the KV file
            video_player = self.ids.get('video_player')
            if video_player:
                # Set the source to the absolute path
                video_player.source = video_path
                print(f"Set video source to: {video_player.source}")
                
                # Bind to state changes; when state becomes 'stop', video is done
                video_player.bind(state=self._on_video_state)
                print(f"Bound to video player. Current state: {video_player.state}")
            else:
                print("VideoPlayer not found")
        except Exception as e:
            print(f"Could not set video source: {e}")
        
        # Fallback timeout: switch to loading after 10 seconds even if video doesn't finish
        Clock.schedule_once(self._go_to_loading_fallback, 10.0)

    def _go_to_loading(self, dt):
        if self.manager:
            try:
                self.manager.current = "loading"
            except Exception as e:
                print(f"Failed to switch to loading screen: {e}")

    def _on_video_state(self, video_player, state):
        """Called when video state changes. Switch to loading when video stops."""
        print(f"Video state: {state}")
        if state == "stop":
            self._go_to_loading(None)

    def _go_to_loading_fallback(self, dt):
        """Fallback: cancel video binding and switch if not already done."""
        try:
            video_player = self.ids.get('video_player')
            if video_player:
                video_player.unbind(state=self._on_video_state)
        except:
            pass
        self._go_to_loading(dt)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return None  # everything is in animation.kv
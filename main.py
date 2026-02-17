import os
import json

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)          
print("Working directory set to:", os.getcwd())


import sys

os.environ["KIVY_NO_ARGS"] = "1"
bypass_login = False
default_user_id = None

# Example usage:
# python main.py --bypass 1
# "--bypass 1" means skip login and use user ID 1

if "--bypass" in sys.argv:
    bypass_index = sys.argv.index("--bypass")
    if len(sys.argv) > bypass_index + 1:
        default_user_id = sys.argv[bypass_index + 1]
        bypass_login = True




from kivymd.app import MDApp
from kivymd.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import FadeTransition
from kivy.lang import Builder
from kivy.uix.image import AsyncImage
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window

# Import screens
from frontend.scripts.loading_screen import LoadingScreen
from frontend.scripts.login_screen import LoginScreen
from frontend.scripts.signup_screen import SignupScreen
from frontend.scripts.home_screen import HomeScreen 
from frontend.scripts.tasks_screen import TasksScreen 
from frontend.scripts.quiz_screen import QuizScreen
from frontend.scripts.profile_screen import ProfileScreen
from frontend.scripts.chatbot_screen import ChatBotScreen
from frontend.scripts.lesson_screen import LessonScreen
from frontend.scripts.lesson_screen import TopicRoadmapScreen
from frontend.scripts.lesson_progress_screen import LessonProgressScreen
from frontend.scripts.quiz_engine import MiniQuestScreen

from kivy.core.audio import SoundLoader
from time import sleep
import threading

configFile = "configFile.json"

if os.path.exists(configFile):
    with open(configFile, 'r') as f:
        config = json.load(f)
        print("Loaded Configartion file Successfully!")

else:
    print("Configaration file not found!!!")

class LuminaScreenManager(ScreenManager):
    pass

#Window.size = (600, 700)

class LuminaApp(MDApp):
    def __init__(self, bypass=False, default_user_id=None, **kwargs):
        super().__init__(**kwargs)
        self.bypass_login = bypass
        self.default_user_id = default_user_id
        self.current_user = None

    # Main application class
    # ------- GLOBAL Assets & Configuration -------
    loading_image = config["Assets"]["loading_image"]
    loading_animation = config["Assets"]["loading_animation"]
    app_logo = config["Assets"]["app_logo"]
    app_logo2 = config["Assets"]["app_logo2"]
    app_icon = config["Assets"]["app_icon"]

    inbox_icon = config["Assets"]["inbox_icon"]
    profile_icon = config["Assets"]["profile_icon"]
    notification_icon = config["Assets"]["notification_icon"]
    tutor_icon = config["Assets"]["tutor_icon"]
    home_icon = config["Assets"]["home_icon"]
    task_icon = config["Assets"]["task_icon"]
    leaderboard_icon = config["Assets"]["leaderboard_icon"]
    menu_icon  = config["Assets"]["menu_icon"]
    quiz_icon = config["Assets"]["quiz_icon"]
    tree_image = config["Assets"]["tree_image"]
    tutor_logo = config["Assets"]["tutor_logo"]

    login_wallpaper = config["Assets"]["login_wallpaper"]
    subject_wallpaper = config["Assets"]["subject_wallpaper"]
    biology_wallpaper = config["Assets"]["biology_wallpaper"]
    quiz_wallpaper = "frontend/assets/images/wallpapers/quiz_wallpaper.jpg"
    timetable_wallpaper = "frontend/assets/images/wallpapers/timetable_wallpaper.jpg"   

    theme1 =  config["Sounds"]["theme1"]
    theme2 =  config["Sounds"]["theme2"]

    def on_start(self):
        self.start_background_music()

        if self.bypass_login and self.default_user_id:
            print(f"Bypass active: logging in as user {self.default_user_id}")
            self.load_user_graphs(self.default_user_id)
            # Skip login screen, go straight to home
            self.root.current = "home"

    def start_background_music(self):
        def play_music():
            sound = SoundLoader.load(self.theme1)
            if sound:
                sound.volume = 0.3
                sound.loop = True
                sound.play()
                print("Background music playing...")
                # Keep thread alive while app is running
                while True:
                    from time import sleep
                    sleep(1)
            else:
                print("Sound file not found!")

        # Start the music in a separate thread
        music_thread = threading.Thread(target=play_music, daemon=True)
        music_thread.start()

    current_user = None
    graphs = []
    current_id = 0
    current_graph = None


    def load_user_graphs(self, user_id):
        self.current_user = str(user_id)  # store current user
        user_folder = os.path.join("data/user", self.current_user)

        if not os.path.exists(user_folder):
            print(f"No folder for user {self.current_user}")
            self.graphs = []
            self.current_graph = None
            return

        self.graphs = [f for f in os.listdir(user_folder) if f.lower().endswith(".png")]
        self.current_id = 0

        if self.graphs:
            self.current_graph = os.path.join(user_folder, self.graphs[0])
            # Update home screen if loaded
            try:
                home_screen = self.root.get_screen("home")
                home_screen.ids.graph_image.source = self.current_graph
                home_screen.ids.graph_image.reload()
            except Exception as e:
                print("Home screen not ready yet:", e)
        else:
            self.current_graph = None

        print(f"User {self.current_user} graphs loaded: {self.graphs}")


    Name = config["AppConfig"]["Name"]
    version = config["AppConfig"]["Version"]

    def graph_back(self):
        if self.current_id > 0:
            self.current_id -= 1
            self.update_graph_image()

    def graph_forward(self):
        if self.current_id < len(self.graphs) - 1:
            self.current_id += 1
            self.update_graph_image()

    def update_graph_image(self):
        if not self.graphs:
            print("No graphs to display")
            return

        home_screen = self.root.get_screen("home")
        home_screen.ids.graph_image.source = os.path.join(
            "data/user", self.current_user, self.graphs[self.current_id]
        )
        home_screen.ids.graph_image.reload()


    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = config["AppConfig"]["Theme"]

        sm = LuminaScreenManager(transition=FadeTransition(duration=0.8))

        self.loading_kivy_path = "frontend/screens/loading.kv"
        try:
            if os.path.exists(self.loading_kivy_path):
                Builder.load_file(self.loading_kivy_path)
                print("Successfully loaded loading.kv")
            else:
                print(f"loading.kv does not exist: {self.loading_kivy_path}")
        except Exception as e:
            print("Error loading \'loading.kv\': {e}")

        # Adding loading screen first, then others
        sm.add_widget(LoadingScreen(name="loading"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SignupScreen(name="signup"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(TasksScreen(name="tasks"))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(QuizScreen(name="quiz"))
        sm.add_widget(ChatBotScreen(name="tutor"))
        sm.add_widget(LessonScreen(name="lesson"))
        sm.add_widget(TopicRoadmapScreen(name='topic_roadmap'))
        sm.add_widget(LessonProgressScreen(name="lesson_progress"))
        sm.add_widget(MiniQuestScreen(name="miniquest"))

        sm.current = "loading"

        return sm  

class ImageButton(ButtonBehavior, AsyncImage):
    pass

if __name__ == "__main__":
    app = LuminaApp(bypass=bypass_login, default_user_id=default_user_id)
    app.run()

from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDIcon

from functools import partial
import json
import os

from kivy.core.text import LabelBase

LabelBase.register(
    name="EmojiFont",
    fn_regular="C:/Windows/Fonts/seguiemj.ttf"
)


'''label = MDLabel(
    text=label_text,
    font_style="H6",
    halign="left",
    font_name="EmojiFont",
)'''



class SubjectCard(MDCard):
    pass

class TopicCard(MDCard):
    def __init__(self, topic, status, callback, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = 130
        self.padding = 15
        self.spacing = 10
        self.radius = [15]
        self.elevation = 5

        # --- Title row (text + icon) ---
        header = MDBoxLayout(
            orientation="horizontal",
            spacing=10,
            adaptive_height=True
        )

        title = MDLabel(
            text=topic["name"],
            font_style="H6",
            halign="left"
        )

        if status == "completed":
            icon = MDIcon(icon="check-circle", theme_text_color="Custom", text_color=(0, 0.8, 0, 1))
        elif status == "locked":
            icon = MDIcon(icon="lock", theme_text_color="Custom", text_color=(0.6, 0.6, 0.6, 1))
        else:
            icon = MDIcon(icon="play-circle", theme_text_color="Custom", text_color=(0.1, 0.6, 0.9, 1))
        
        header.add_widget(title)
        header.add_widget(icon)

        self.add_widget(header)

        # --- Description ---
        desc = MDLabel(
            text=topic.get("short_description", ""),
            font_style="Body1",
            halign="left"
        )
        self.add_widget(desc)

        # --- Start button (ONLY for next topic) ---
        if status == "next":
            btn = MDRaisedButton(
                text="Start",
                size_hint=(None, None),
                size=(120, 40)
            )
            btn.bind(on_release=lambda x: callback(topic["id"]))
            self.add_widget(btn)


class LessonScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user = None
        self.app = MDApp.get_running_app()

    def on_enter(self, *args):
        app = MDApp.get_running_app()
        self.current_user = app.current_user
        self.load_subjects()

    def load_subjects(self):
        self.ids.lesson_content.clear_widgets()
        json_path = f"data/user/{self.current_user}/progress/user_progress.json"

        if not os.path.exists(json_path):
            print("user_progress.json not found!")
            return

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        subjects = data.get("subjects", [])
        # support legacy format keyed by user id
        if not subjects and isinstance(data, dict) and self.current_user in data:
            subjects = data[self.current_user].get("subjects", [])

        for subj in subjects:
            card = SubjectCard()  # instantiate Python class
            card.ids.title.text = f"{subj.get('name', 'Unknown')} {subj.get('emoji', '')}"
            card.ids.description.text = subj.get("description", "")
            lessons = max(subj.get("lessons", 0), 1)
            completed = subj.get("completed", 0)
            card.ids.progress.value = (completed / lessons) * 100

            btn = MDFlatButton(text="Select ▶", size_hint_y=None, height=36, font_name="C:/Windows/Fonts/seguiemj.ttf", theme_text_color="Custom", text_color=(0, 0, 0, 1))
            btn.bind(on_release=partial(self.select_subject, subj.get("id")))
            card.add_widget(btn)  # add button to the bottom of the card

            self.ids.lesson_content.add_widget(card)

            '''card.ids.select_btn.bind(
                on_release=lambda x, sid=subj["id"]: self.select_subject(sid)
            )

            self.ids.lesson_content.add_widget(card)'''

    def select_subject(self, subject_id, *kwargs):
        # Navigate to Topic Roadmap
        self.app.switch_to("topic_roadmap")
        # self.app.screen_manager is the correct manager instance (LuminaApp has no 'manager')
        roadmap_screen = self.app.screen_manager.get_screen("topic_roadmap")
        roadmap_screen.subject_id = subject_id
        roadmap_screen.load_roadmap(subject_id)

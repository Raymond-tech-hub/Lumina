from kivy.lang import Builder
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

        user_data = data.get(self.current_user, {})
        subjects = user_data.get("subjects", [])

        for subj in subjects:
            card = SubjectCard()  # instantiate Python class
            card.ids.title.text = f"{subj['name']} {subj['emoji']}"
            card.ids.description.text = subj["description"]
            card.ids.progress.value = (subj["completed"] / subj["lessons"]) * 100

            btn = MDFlatButton(text="Select ▶", size_hint_y=None, height=36, font_name="C:/Windows/Fonts/seguiemj.ttf", theme_text_color="Custom", text_color=(0, 0, 0, 1))
            btn.bind(on_release=partial(self.select_subject, subj["id"]))
            card.add_widget(btn)  # add button to the bottom of the card

            self.ids.lesson_content.add_widget(card)

            '''card.ids.select_btn.bind(
                on_release=lambda x, sid=subj["id"]: self.select_subject(sid)
            )

            self.ids.lesson_content.add_widget(card)'''

    def select_subject(self, subject_id, *kwargs):
        # Navigate to Topic Roadmap
        self.manager.current = "topic_roadmap"
        roadmap_screen = self.manager.get_screen("topic_roadmap")
        roadmap_screen.subject_id = subject_id
        roadmap_screen.load_roadmap(subject_id)


# -----------------------------
# Topic Roadmap Screen
# -----------------------------
class TopicRoadmapScreen(MDScreen):
    subject_id = None
    current_user = None

    def load_roadmap(self, subject_id):
        self.ids.roadmap_container.clear_widgets()
        app = MDApp.get_running_app()
        self.current_user = app.current_user

        # Load user progress
        user_json = f"data/user/{self.current_user}/progress/user_progress.json"
        with open(user_json, "r", encoding='utf-8') as f:
            user_data = json.load(f)
        subject_progress = next((s for s in user_data[self.current_user]["subjects"] if s["id"]==subject_id), None)
        completed_count = subject_progress["completed"]

        # Load subject topics
        subject_json = f"data/user/{self.current_user}/subjects/course_{subject_id}.json"
        with open(subject_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        topics = data["topics"]

        for idx, topic in enumerate(topics):
            if idx < completed_count:
                status = "completed"
            elif idx == completed_count:
                status = "next"
            else:
                status = "locked"

            card = TopicCard(topic, status, self.start_topic)
            self.ids.roadmap_container.add_widget(card)

    def start_topic(self, topic_id):
        print(f"Starting topic: {topic_id}")
        # Navigate to lesson progress screen
        self.manager.current = "lesson_progress"
        progress_screen = self.manager.get_screen("lesson_progress")
        progress_screen.load_lesson(self.subject_id, topic_id)


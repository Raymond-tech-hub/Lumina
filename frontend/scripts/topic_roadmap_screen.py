from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivy.core.text import LabelBase, partial
from kivymd.uix.boxlayout import MDBoxLayout 
#import MD icons
from kivymd.uix.label import MDIcon   

import json
import os

LabelBase.register(
    name="EmojiFont",
    fn_regular="C:/Windows/Fonts/seguiemj.ttf"
)

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


class TopicRoadmapScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
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

        subjects = user_data.get("subjects", [])
        if not subjects and isinstance(user_data, dict) and self.current_user in user_data:
            subjects = user_data[self.current_user].get("subjects", [])

        subject_progress = next((s for s in subjects if s.get("id") == subject_id), None)
        completed_count = subject_progress.get("completed", 0) if subject_progress else 0

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
        app = MDApp.get_running_app()
        print(f"Starting topic: {topic_id}")
        # Navigate to lesson progress screen
        app.switch_to("lesson_progress")
        #self.manager.current = "lesson_progress"
        progress_screen = self.app.screen_manager.get_screen("lesson_progress")
        progress_screen.load_lesson(self.subject_id, topic_id)


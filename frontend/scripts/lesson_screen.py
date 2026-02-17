import os
import json
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

class LessonScreen(MDScreen):
    current_user = "001"  # Example: can be dynamically set from login

    def on_enter(self, *args):
        """Called when entering the lesson screen"""
        self.load_subjects()

    def load_subjects(self):
        self.ids.lesson_content.clear_widgets()
        json_path = f"data/user/{self.current_user}/user_progress.json"

        if not os.path.exists(json_path):
            print("user_progress.json not found!")
            return

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        user_data = data.get(self.current_user, {})
        subjects = user_data.get("subjects", [])

        for subj in subjects:
            # Load card from KV template
            card = Builder.load_string("SubjectCard:")
            card.ids.title.text = f"{subj['name']} {subj['emoji']}"
            card.ids.description.text = subj["description"]
            card.ids.progress.value = (subj["completed"] / subj["lessons"]) * 100
            card.ids.select_btn.bind(
                on_release=lambda x, sid=subj["id"]: self.select_subject(sid)
            )

            self.ids.lesson_content.add_widget(card)

    def select_subject(self, subject_id):
        print(f"Selected subject: {subject_id}")
        # Load the corresponding course JSON
        course_file = f"frontend/assets/data/course_{subject_id}.json"
        if os.path.exists(course_file):
            with open(course_file, "r", encoding="utf-8") as f:
                self.course_data = json.load(f)
            self.manager.current = "lesson_topic"
        else:
            print(f"Course file not found: {course_file}")
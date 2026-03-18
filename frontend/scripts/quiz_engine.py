# mini_quest.py
import os
import json
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.screen import MDScreen

from backend.tree import Tree

class MiniQuestScreen(MDScreen):
    content_box = ObjectProperty(None)

    def __init__(self, subject="biology", topic_id="osmosis_101", **kwargs):
        super().__init__(**kwargs)
        self.subject = subject
        self.topic_id = topic_id
        self.quiz_index = 0
        self.score = 0

        MAIN_DIR = os.getcwd()
        self.json_path = os.path.join(MAIN_DIR, "data", "sample_quiz.json")

        # Load JSON
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                self.course_data = json.load(f)
        except Exception as e:
            raise FileNotFoundError(f"Cannot load {self.json_path}: {e}")

        self.topic = self.get_topic(subject, topic_id)
        self.total = len(self.topic.get("quiz", []))

    def on_enter(self, *args):
        app = MDApp.get_running_app()
        self.current_user = app.current_user   
        self.user_tree = Tree(self.current_user)
        
        self.build_question()

    def get_topic(self, subject, topic_id):
        subject_data = self.course_data.get("subjects", {}).get(subject, {})
        for topic in subject_data.get("topics", []):
            if topic.get("id") == topic_id:
                if "quiz" not in topic and "questions" in topic:
                    topic["quiz"] = topic["questions"]
                return topic
        raise ValueError(f"Topic {topic_id} not found in {subject}")

    def build_question(self):
        """Update content_box for current question"""
        self.content_box.clear_widgets()

        # Add mini lesson/context
        for line in self.topic.get("content", []):
            lbl = MDLabel(text=line, adaptive_height=True, font_name="C:/Windows/Fonts/seguiemj.ttf")
            self.content_box.add_widget(lbl)

        # Diagram
        diagram_file = self.topic.get("diagram")
        if diagram_file:
            diagram_path = os.path.join(os.path.dirname(self.json_path), "assets", diagram_file)
            if os.path.exists(diagram_path):
                img = Image(source=diagram_path, size_hint_y=None, height=250, allow_stretch=True, keep_ratio=True)
                self.content_box.add_widget(img)

        # Check if quiz is finished
        if self.quiz_index >= self.total:
            bonus_xp = 25
            self.user_tree.add_xp(bonus_xp)

            self.content_box.add_widget(MDLabel(
                text=f"🎉 Mini Quest Completed!\nScore: {self.score}/{self.total}\n🌱 +{bonus_xp} XP Bonus!",
                adaptive_height=True,
                font_name="C:/Windows/Fonts/seguiemj.ttf"
            ))
            return


        # Current question
        self.current_question = self.topic["quiz"][self.quiz_index]
        question_lbl = MDLabel(
            text=f"Q{self.quiz_index + 1}: {self.current_question['question']}",
            adaptive_height=True,
            font_name="C:/Windows/Fonts/seguiemj.ttf"
        )
        self.content_box.add_widget(question_lbl)

        # Option buttons
        for option in self.current_question["options"]:
            btn = MDRaisedButton(text=option, size_hint=(1, None), height=50)
            btn.bind(on_press=self.check_answer)
            self.content_box.add_widget(btn)

        # Hint button
        hint_btn = MDRaisedButton(text="💡 Hint", size_hint=(1, None), height=50, font_name="C:/Windows/Fonts/seguiemj.ttf")
        hint_btn.bind(on_press=self.show_hint)
        self.content_box.add_widget(hint_btn)

        # Progress bar
        self.content_box.add_widget(MDProgressBar(max=self.total, value=self.quiz_index, height=20))

    def show_hint(self, instance):
        hint = self.current_question.get("hint", "No hint available.")
        popup = Popup(
            title="Hint",
            content=MDLabel(text=hint, adaptive_height=True, font_name="C:/Windows/Fonts/seguiemj.ttf"),
            size_hint=(0.6, 0.4)
        )
        popup.open()

    def check_answer(self, instance):
        selected = instance.text
        correct = self.current_question["answer"]

        feedback = "Correct! " if selected == correct else f"Wrong!. Correct: {correct}"
        if selected == correct:
            self.score += 1

            points_for_correct = 10  # same XP rule
            self.user_tree.add_xp(points_for_correct)
            print(f"[MiniQuest] Added {points_for_correct} XP to user {self.current_user}")

        popup = Popup(
            title="Feedback",
            content=MDLabel(text=feedback, adaptive_height=True, font_name="C:/Windows/Fonts/seguiemj.ttf"),
            size_hint=(0.6, 0.4)
        )
        popup.open()

        self.quiz_index += 1
        self.build_question()

    def go_back(self):
        if self.manager:
            self.manager.current = "home"


class MiniQuestApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return MiniQuestScreen(subject="biology", topic_id="osmosis_101")

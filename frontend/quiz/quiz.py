# quiz.py

import os
import json
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton  # Compatible with 1.2.0
from kivymd.uix.progressbar import MDProgressBar

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load course content JSON
with open(os.path.join(BASE_DIR, "course_data.json")) as f:
    course_data = json.load(f)

# Load user progress JSON if exists, otherwise create empty
progress_path = os.path.join(BASE_DIR, "user_progress.json")
if os.path.exists(progress_path):
    with open(progress_path) as f:
        user_progress = json.load(f)
else:
    user_progress = {}

# For simplicity, start with first topic of biology
subject = "biology"
topic_data = course_data['subjects'][subject]['topics'][0]
topic_id = topic_data['id']


class QuizScreen(BoxLayout):
    scroll_view = ObjectProperty(None)
    content_box = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.topic = topic_data
        self.quiz_index = 0
        self.score = 0
        self.total = len(self.topic['quiz'])
        self.build_screen()

    def build_screen(self):
        self.clear_widgets()

        # Scrollable area
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.content_box = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=10,
            padding=10
        )
        self.content_box.bind(minimum_height=self.content_box.setter('height'))
        self.scroll_view.add_widget(self.content_box)
        self.add_widget(self.scroll_view)

        # Mini lesson / context
        for line in self.topic.get('content', []):
            lbl = MDLabel(
                text=line,
                size_hint_y=None,
                adaptive_height=True,
                theme_text_color="Primary"
            )
            self.content_box.add_widget(lbl)

        # Diagram if available
        diagram_file = self.topic.get('diagram', None)
        diagram_path = os.path.join(BASE_DIR, "assets", diagram_file) if diagram_file else None
        if diagram_path and os.path.exists(diagram_path):
            img = Image(
                source=diagram_path,
                size_hint_y=None,
                height=250,
                allow_stretch=True,
                keep_ratio=True
            )
            self.content_box.add_widget(img)

        # Current quiz question
        if self.quiz_index >= self.total:
            self.content_box.add_widget(MDLabel(
                text=f"Quiz Completed! Score: {self.score}/{self.total}",
                size_hint_y=None,
                adaptive_height=True,
                theme_text_color="Primary"
            ))
            return

        self.current_question = self.topic['quiz'][self.quiz_index]
        question_lbl = MDLabel(
            text=f"Question {self.quiz_index+1}: {self.current_question['question']}",
            size_hint_y=None,
            adaptive_height=True,
            theme_text_color="Primary"
        )
        self.content_box.add_widget(question_lbl)

        # Option buttons
        self.option_buttons = []
        for option in self.current_question['options']:
            btn = MDRaisedButton(
                text=option,
                size_hint=(1, None),
                height=50,
            )
            btn.bind(on_press=self.check_answer)
            self.option_buttons.append(btn)
            self.content_box.add_widget(btn)

        # Hint button
        hint_btn = MDRaisedButton(
            text="💡 Hint",
            size_hint=(1, None),
            height=50,
        )
        hint_btn.bind(on_press=self.show_hint)
        self.content_box.add_widget(hint_btn)

        # Progress bar
        self.progress = MDProgressBar(
            max=self.total,
            value=self.quiz_index,
            size_hint_y=None,
            height=20
        )
        self.content_box.add_widget(self.progress)

    def show_hint(self, instance):
        hint = self.current_question.get('hint', "No hint available.")
        popup = Popup(
            title="Hint",
            content=MDLabel(text=hint, adaptive_height=True),
            size_hint=(0.6, 0.4)
        )
        popup.open()

    def check_answer(self, instance):
        selected = instance.text
        correct = self.current_question['answer']
        if selected == correct:
            self.score += 1
            feedback = "Correct! ✅"
        else:
            feedback = f"Wrong ❌. Correct: {correct}"

        popup = Popup(
            title="Feedback",
            content=MDLabel(text=feedback, adaptive_height=True),
            size_hint=(0.6, 0.4)
        )
        popup.open()

        # Next question
        self.quiz_index += 1
        self.build_screen()


class QuizApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return QuizScreen()


if __name__ == "__main__":
    QuizApp().run()

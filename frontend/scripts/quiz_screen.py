
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
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.animation import Animation

from backend.tree import Tree


class QuizScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.json_path = "data/sample_quiz.json"
        self.quiz_index = 0   # current question
        self.score = 0        # total correct answers
        self.questions = []  

    def on_enter(self, *args):
        print("Quiz screen entered")
        Clock.schedule_once(self._pulse_logo, 0.8)

        # Load JSON
        self.load()

        # Pick a subject and topic
        subject = "biology"
        topic_index = 0  # first topic

        self.questions = self.get_topic_quiz(subject, topic_index)
        self.quiz_index = 0
        self.score = 0

        app = MDApp.get_running_app()
        self.current_user = app.current_user
        self.user_tree = Tree(self.current_user)

        # Display first question
        self.display_question()


    def _pulse_logo(self, dt):
        logo = self.ids.get('logo')
        if logo:
            anim = (Animation(opacity=0.45, duration=1.0, t='out_quad') +
                    Animation(opacity=1.0, duration=1.0, t='out_quad'))
            anim.repeat = True
            anim.start(logo)

    def go_home(self):
        self.manager.current = "home"

    def go_profile(self):
        print("entering profile")
        self.manager.current = "profile"

    def go_tasks(self):
        print("entering tasks")
        self.manager.current = "tasks"

    def go_quiz(self):
        print("entering quiz")
        self.manager.current = "quiz"

    def go_leaderboard(self):
        print("entering leaderboard")
        self.manager.current = "leaderboard"

    def go_tutor(self):
        print("entering tutor")
        self.manager.current = "tutor"

    
    def load(self):
        """Load the JSON into self.data"""
        with open(self.json_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        return self.data

    def get_subject_topics(self, subject_name):
        """Return list of topics for a subject"""
        if not self.data:
            self.load()
        return self.data["subjects"].get(subject_name, {}).get("topics", [])

    def get_topic_quiz(self, subject_name, topic_index=0):
        """Return the quiz list for a topic"""
        topics = self.get_subject_topics(subject_name)
        if not topics:
            return []
        topic = topics[topic_index]
        return topic.get("questions", [])

    '''def on_enter(self):
        # Load JSON
        self.load()

        # Pick a subject and topic
        subject = "biology"
        topic_index = 0  # first topic

        self.questions = self.get_topic_quiz(subject, topic_index)
        self.quiz_index = 0
        self.score = 0

        # Display first question
        self.display_question()'''

    def display_question(self):
        container = self.ids.quiz_container
        container.clear_widgets()

        if self.quiz_index >= len(self.questions):
            # Quiz finished
            container.add_widget(MDLabel(
                text=f"Quiz Completed!\nScore: {self.score}/{len(self.questions)}",
                halign="center",
                adaptive_height=True
            ))
            return

        q = self.questions[self.quiz_index]

        # Question
        container.add_widget(MDLabel(
            text=f"Q{self.quiz_index+1}: {q['question']}",
            adaptive_height=True,
            theme_text_color="Primary"
        ))

        # Options
        for option in q["options"]:
            btn = MDRaisedButton(
                text=option,
                size_hint_y=None,
                height=48
            )
            btn.bind(on_release=self.check_answer)
            container.add_widget(btn)

    def check_answer(self, instance):
        selected = instance.text
        correct = self.questions[self.quiz_index]["answer"]

        if selected == correct:
            self.score += 1

            # Add XP to user's tree
            points_for_correct = 10  # 10 XP per correct answer
            self.user_tree.add_xp(points_for_correct)
            print(f"Added {points_for_correct} XP to user {self.current_user}!")

        self.quiz_index += 1
        self.display_question()


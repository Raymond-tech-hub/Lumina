import os
import json
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp

class TopicOverviewScreen(MDScreen):
    
    def set_topic(self, topic, subject_id):
        self.subject_id = subject_id
        self.topic = topic
        self.ids.overview_title.text = topic.get("name", "")
        self.ids.overview_description.text = topic.get("short_description", "")

    def build_ui(self):
        layout = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(20))
        
        from kivymd.uix.card import MDCard

        card = MDCard(
            orientation="vertical",
            padding=dp(20),
            radius=[15,],
            elevation=10,
            size_hint=(0.9, None),
            height=dp(200),
            pos_hint={"center_x": 0.5}
        )

        # Title
        self.title_label = MDLabel(
            text=self.topic.get("name", ""),
            font_style="H6",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.1, 0.6, 0.9, 1)
        )
        card.add_widget(self.title_label)

        # Short description
        self.desc_label = MDLabel(
            text=self.topic.get("short_description", ""),
            font_style="Body1",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint_y=None
        )
        self.desc_label.height = self.desc_label.texture_size[1]
        card.add_widget(self.desc_label)

        # Begin button
        begin_btn = MDRaisedButton(
            text="Begin ▶",
            md_bg_color=(0.1, 0.6, 0.9, 1),
            pos_hint={"center_x": 0.5},
            on_release=self.begin_lesson
        )
        card.add_widget(begin_btn)

        layout.add_widget(card)
        self.add_widget(layout)

    def begin_lesson(self, *args):
        """Navigate to the LessonProgressScreen for this topic"""
        if self.subject_id and self.topic:
            lesson_screen = self.app.get_screen("lesson_progress")
            lesson_screen.load_lesson(self.subject_id, self.topic["id"])
            self.app.switch_to("lesson_progress")
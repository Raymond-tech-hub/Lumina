# mini_quest.py
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
import os
import json



class MiniQuestScreen(MDScreen):
    scroll_view = ObjectProperty(None)
    content_box = ObjectProperty(None)

    class MiniQuestScreen(MDScreen):
        scroll_view = ObjectProperty(None)
        content_box = ObjectProperty(None)

        def __init__(self, subject: str = "biology", topic_id: str = "osmosis_101", **kwargs):
            super().__init__(**kwargs)
            self.subject = subject
            self.topic_id = topic_id
            self.quiz_index = 0
            self.score = 0

            # Use main.py directory as base
            MAIN_DIR = os.getcwd()  # this is the directory where main.py is run
            self.json_path = os.path.join(MAIN_DIR, "data", "user", "sample_quiz.json")

            # Load course content JSON
            try:
                with open(self.json_path, "r", encoding="utf-8") as f:
                    self.course_data = json.load(f)
                    print("Loaded mini quest quiz json")
            except Exception as e:
                raise FileNotFoundError(f"Could not load {self.json_path}: {e}")

            # Now retrieve topic dynamically
            self.topic = self.get_topic(subject, topic_id)
            self.total = len(self.topic.get("quiz", []))

            # Build the screen
            self.build_screen()


    def get_topic(self, subject: str, topic_id: str):
        """Retrieve topic data from JSON using topic_id."""
        subject_data = self.course_data.get("subjects", {}).get(subject, {})
        for topic in subject_data.get("topics", []):
            if topic.get("id") == topic_id:
                # Normalize quiz key if necessary
                if "quiz" not in topic and "questions" in topic:
                    topic["quiz"] = topic["questions"]
                return topic
        raise ValueError(f"Topic '{topic_id}' not found for subject '{subject}'")

    def build_screen(self):
        self.clear_widgets()

        # Scrollable area
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.content_box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=10,
            padding=10
        )
        self.content_box.bind(minimum_height=self.content_box.setter("height"))
        self.scroll_view.add_widget(self.content_box)
        self.add_widget(self.scroll_view)

        # Mini lesson / context
        for line in self.topic.get("content", []):
            lbl = MDLabel(
                text=line,
                size_hint_y=None,
                adaptive_height=True,
                font_name="C:/Windows/Fonts/seguiemj.ttf",  # Emoji support
            )
            self.content_box.add_widget(lbl)

        # Diagram if available
        diagram_file = self.topic.get("diagram")
        diagram_path = os.path.join(self.json_path, "assets", diagram_file) if diagram_file else None
        if diagram_path and os.path.exists(diagram_path):
            img = Image(
                source=diagram_path,
                size_hint_y=None,
                height=250,
                allow_stretch=True,
                keep_ratio=True
            )
            self.content_box.add_widget(img)

        # Show quiz question
        if self.quiz_index >= self.total:
            self.content_box.add_widget(MDLabel(
                text=f"🎉 Mini Quest Completed! Score: {self.score}/{self.total}",
                size_hint_y=None,
                adaptive_height=True,
                font_name="C:/Windows/Fonts/seguiemj.ttf"
            ))
            return

        self.current_question = self.topic["quiz"][self.quiz_index]

        question_lbl = MDLabel(
            text=f"Q{self.quiz_index+1}: {self.current_question['question']}",
            size_hint_y=None,
            adaptive_height=True,
            font_name="C:/Windows/Fonts/seguiemj.ttf"
        )
        self.content_box.add_widget(question_lbl)

        # Option buttons
        self.option_buttons = []
        for option in self.current_question["options"]:
            btn = MDRaisedButton(
                text=option,
                size_hint=(1, None),
                height=50
            )
            btn.bind(on_press=self.check_answer)
            self.option_buttons.append(btn)
            self.content_box.add_widget(btn)

        # Hint button
        hint_btn = MDRaisedButton(
            text="💡 Hint",
            size_hint=(1, None),
            height=50
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

        if selected == correct:
            self.score += 1
            feedback = "Correct! ✅"
        else:
            feedback = f"Wrong ❌. Correct: {correct}"

        popup = Popup(
            title="Feedback",
            content=MDLabel(text=feedback, adaptive_height=True, font_name="C:/Windows/Fonts/seguiemj.ttf"),
            size_hint=(0.6, 0.4)
        )
        popup.open()

        # Next question
        self.quiz_index += 1
        self.build_screen()

    def go_back(self):
        """Go back to home screen (requires ScreenManager)."""
        if self.manager:
            self.manager.current = "home" 

class MiniQuestApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        # Example: load the osmosis_101 topic
        return MiniQuestScreen(subject="biology", topic_id="osmosis_101")


if __name__ == "__main__":
    MiniQuestApp().run()

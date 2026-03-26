import os
import json
import time
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp
from kivy.uix.popup import Popup

class LessonProgressScreen(MDScreen):
    subject_id = None
    topic_id = None
    current_user = None
    user_progress = {}
    subtopic_start_time = None       # Track start time of each subtopic
    typical_times = {}  

    def load_progress(self):
        """Load user progress from JSON"""
        progress_file = f"data/user/{self.current_user}/progress/user_progress.json"
        if os.path.exists(progress_file):
            with open(progress_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, dict) and self.current_user in data and isinstance(data[self.current_user], dict):
                self.user_progress = data[self.current_user]
            else:
                self.user_progress = data
        else:
            self.user_progress = {}

    def save_progress(self):
        """Save user progress to JSON"""
        if self.subtopic_index < len(self.subtopics) - 1:
            return

        progress_file = f"data/user/{self.current_user}/progress/user_progress.json"
        data = {}
        if os.path.exists(progress_file):
            try:
                with open(progress_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}

        subjects = []
        if isinstance(data, dict):
            subjects = data.get("subjects", [])
            if not subjects and self.current_user in data and isinstance(data[self.current_user], dict):
                subjects = data[self.current_user].get("subjects", [])

        if not isinstance(subjects, list):
            subjects = []

        subject = next((s for s in subjects if s.get("id") == self.subject_id), None)
        if subject is None:
            subject = {
                "id": self.subject_id,
                "name": self.subject_id.capitalize(),
                "emoji": "",
                "lessons": 0,
                "completed": 0,
                "description": "",
                "completed_topic_ids": []
            }
            subjects.append(subject)

        # Sync from course file
        course_path = f"data/user/{self.current_user}/subjects/course_{self.subject_id}.json"
        if os.path.exists(course_path):
            try:
                with open(course_path, "r", encoding="utf-8") as f:
                    course = json.load(f)
                subject["lessons"] = len(course.get("topics", []))
                subj_info = course.get("subject", {})
                subject.update({
                    "name": subj_info.get("name", subject.get("name", "")),
                    "emoji": subj_info.get("emoji", subject.get("emoji", "")),
                    "description": subj_info.get("description", subject.get("description", ""))
                })
            except Exception:
                pass

        completed_topic_ids = subject.setdefault("completed_topic_ids", [])
        if self.topic_id and self.topic_id not in completed_topic_ids:
            completed_topic_ids.append(self.topic_id)

        subject["completed"] = min(len(completed_topic_ids), max(subject.get("lessons", 0), len(completed_topic_ids)))

        output_data = {"subjects": subjects}
        with open(progress_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=4)

    def load_lesson(self, subject_id, topic_id):
        app = MDApp.get_running_app()
        self.current_user = app.current_user
        self.load_progress()

        self.subject_id = subject_id
        self.topic_id = topic_id
        self.subtopic_index = 0

        # Load topic JSON
        path = f"data/user/{self.current_user}/subjects/course_{subject_id}.json"
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.topic = next(t for t in data["topics"] if t["id"] == topic_id)
        self.subtopics = self.topic["content"]

        self.show_subtopic()

    def show_meta_notification(self, title, reason):
        """Show a temporary AI-style feedback snackbar"""
        
        # Create the snackbar instance
        snackbar = MDSnackbar(
            duration=3,
            md_bg_color=(0.1, 0.6, 0.9, 0.95),
            radius=[15, 15, 15, 15],
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5, "bottom": 0.05},
        )
        
        # Add a standard MDLabel as the content
        content = MDLabel(
            text=f"[b]{title}[/b]\n{reason}",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            markup=True, # Allows the [b] bold tags
            halign="left",
        )
        
        snackbar.add_widget(content)
        snackbar.open()

    def show_subtopic(self):
        sub = self.subtopics[self.subtopic_index]

        # ---------- START TIMER ----------
        self.subtopic_start_time = time.time()

        # Determine typical reading time for subtopic
        if sub["text"].startswith("[") and sub["text"].endswith("]"):
            self.typical_times[self.subtopic_index] = 10  # 40 sec for diagrams
        else:
            self.typical_times[self.subtopic_index] = max(10, len(sub["text"]) // 5)

        self.ids.lesson_title.text = self.topic["name"]
        self.ids.subtopic_title.text = sub["subtopic"]

        # Handle diagrams vs text
        if sub["text"].startswith("[") and sub["text"].endswith("]"):
            image_name = sub["text"][1:-1]
            self.ids.lesson_image.source = f"data/user/{self.current_user}/lesson_images/{image_name}"
            self.ids.lesson_image.height = dp(560)
            self.ids.lesson_image.width = dp(560)
            self.ids.lesson_image.opacity = 1
            self.ids.lesson_text.text = ""
        else:
            parsed_text = self.parse_rich_text(sub["text"])
            self.ids.lesson_text.text = parsed_text
            self.ids.lesson_image.opacity = 0

        self.update_progress()

    def update_progress(self):
        total = len(self.subtopics)
        current = self.subtopic_index + 1
        self.ids.progress_label.text = f"{current} / {total}"

    def next_subtopic(self):
        # ---------- CALCULATE ELAPSED TIME ----------
        elapsed = time.time() - self.subtopic_start_time
        typical = self.typical_times.get(self.subtopic_index, 30)

        # Show AI-style feedback
        if elapsed < typical * 0.5:
            self.show_meta_notification(
                "You are moving too fast! ⏩",
                "Taking more time helps you retain key concepts."
            )
        elif elapsed > typical * 2:
            self.show_meta_notification(
                "You are moving slowly 🐢",
                "Consider reviewing the main points to stay on track."
            )
        # --------------------------------------------
        # Save progress before moving
        self.save_progress()

        if self.subtopic_index < len(self.subtopics) - 1:
            self.subtopic_index += 1
            self.show_subtopic()
        else:
            self.finish_lesson()

    def prev_subtopic(self):
        if self.subtopic_index > 0:
            self.subtopic_index -= 1
            self.show_subtopic()

    def finish_lesson(self):
        # Mark final progress
        self.save_progress()

        self.manager.current = "miniquest"
        '''quiz_screen = self.manager.get_screen("quiz")
        quiz_screen.load_quiz(self.subject_id, self.topic_id)'''

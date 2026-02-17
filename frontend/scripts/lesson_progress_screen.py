import os
import json
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp

class LessonProgressScreen(MDScreen):
    subject_id = None
    topic_id = None
    current_user = None
    user_progress = {}

    def load_progress(self):
        """Load user progress from JSON"""
        progress_file = f"data/user/{self.current_user}/progress/user_progress.json"
        if os.path.exists(progress_file):
            with open(progress_file, "r", encoding="utf-8") as f:
                self.user_progress = json.load(f)
        else:
            self.user_progress = {}

    def save_progress(self):
        """Save user progress to JSON"""
        if self.subtopic_index < len(self.subtopics) - 1:
            return
        progress_file = f"data/user/{self.current_user}/progress/user_progress.json"

        # Load current progress
        data = {"subjects": []}
        if os.path.exists(progress_file):
            try:
                with open(progress_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except:
                pass  # corrupt file → start fresh

        # Find or create the subject entry
        subjects = data.setdefault("subjects", [])
        subject = None
        for s in subjects:
            if s.get("id") == self.subject_id:
                subject = s
                break

        if subject is None:
            subject = {
                "id": self.subject_id,
                "name": self.subject_id.capitalize(),
                "emoji": "",
                "lessons": 0,
                "completed": 0,
                "description": ""
            }
            subjects.append(subject)

        # Optional: sync real lesson count from course file (very useful)
        if subject["lessons"] == 0:
            course_path = f"data/user/{self.current_user}/subjects/course_{self.subject_id}.json"
            if os.path.exists(course_path):
                try:
                    with open(course_path, "r", encoding="utf-8") as f:
                        course = json.load(f)
                    subject["lessons"] = len(course.get("topics", []))
                    subj_info = course.get("subject", {})
                    subject.update({
                        "name": subj_info.get("name", subject["name"]),
                        "emoji": subj_info.get("emoji", subject["emoji"]),
                        "description": subj_info.get("description", subject["description"])
                    })
                except:
                    pass  # silent fail

        # Now increment completed (with safety cap)
        current = subject.get("completed", 0)
        max_lessons = subject.get("lessons", 999)
        if current < max_lessons:
            subject["completed"] = current + 1

        # Save back
        with open(progress_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

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

    def show_subtopic(self):
        sub = self.subtopics[self.subtopic_index]

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
            self.ids.lesson_text.text = sub["text"]
            self.ids.lesson_image.opacity = 0

        self.update_progress()

    def update_progress(self):
        total = len(self.subtopics)
        current = self.subtopic_index + 1
        self.ids.progress_label.text = f"{current} / {total}"

    def next_subtopic(self):
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

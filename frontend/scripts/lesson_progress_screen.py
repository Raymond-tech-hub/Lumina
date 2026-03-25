import os
import json
import time
import re

from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp

class LessonProgressScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()
    subject_id = None
    topic_id = None
    current_user = None
    user_progress = {}
    subtopic_start_time = None       # Track start time of each subtopic
    typical_times = {}  

    def parse_rich_text(self, text):
        """Parse custom tags into Kivy markup"""

        if not text:
            return ""

        # Enable markup
        parsed = text

        # ---------------- HEADINGS ----------------
        parsed = re.sub(
            r"<h1>(.*?)</h1>",
            r"[size=28sp][b]\1[/b][/size]",
            parsed,
            flags=re.DOTALL
        )

        parsed = re.sub(
            r"<h2>(.*?)</h2>",
            r"[size=22sp][b]\1[/b][/size]",
            parsed,
            flags=re.DOTALL
        )

        # ---------------- HIGHLIGHT ----------------
        def highlight_replacer(match):
            color = match.group(1)
            content = match.group(2)

            color_map = {
                "yellow": "ffcc00",
                "blue": "4da6ff",
                "green": "33cc99",
                "red": "ff3333"
            }

            hex_color = color_map.get(color, "ffff00")
            return f"[color={hex_color}][b]{content}[/b][/color]"

        parsed = re.sub(
            r"<highlight=(.*?)>(.*?)</highlight>",
            highlight_replacer,
            parsed,
            flags=re.DOTALL
        )

        return parsed

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
        """Save user progress to JSON, with subtopic-level tracking and topic-overview metadata"""
        
        progress_file = f"data/user/{self.current_user}/progress/user_progress.json"

        # Load existing progress
        data = {}
        if os.path.exists(progress_file):
            try:
                with open(progress_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}

        # Ensure subjects list exists
        subjects = data.get("subjects", []) if isinstance(data, dict) else []
        if not isinstance(subjects, list):
            subjects = []

        # Find or create current subject entry
        subject = next((s for s in subjects if s.get("id") == self.subject_id), None)
        if subject is None:
            subject = {
                "id": self.subject_id,
                "name": self.subject_id.capitalize(),
                "emoji": "",
                "lessons": 0,
                "completed": 0,
                "description": "",
                "difficulty": "Medium",
                "estimated_time": 0,
                "current_subtopic": 0,
                "completed_topic_ids": []
            }
            subjects.append(subject)

        # Save current subtopic index (always)
        subject["current_subtopic"] = self.subtopic_index

        # Load overview JSON for metadata
        overview_path = f"data/user/{self.current_user}/subjects/{self.subject_id}/{self.subject_id}.json"
        if os.path.exists(overview_path):
            try:
                with open(overview_path, "r", encoding="utf-8") as f:
                    overview = json.load(f)

                topic_meta = next((t for t in overview.get("topics", []) if t["id"] == self.topic_id), {})

                # Update general subject info
                subject["lessons"] = len(overview.get("topics", []))
                subject["name"] = overview.get("subject", {}).get("name", subject["name"])
                subject["emoji"] = overview.get("subject", {}).get("emoji", subject["emoji"])
                subject["description"] = overview.get("subject", {}).get("description", subject["description"])

                # Update topic-specific metadata
                subject["difficulty"] = topic_meta.get("difficulty", "Medium")
                subject["estimated_time"] = topic_meta.get("estimated_time", 10)  # default 10 min
            except Exception:
                pass

        # Mark topic complete if last subtopic reached
        if self.subtopic_index >= len(self.subtopics) - 1:
            completed_topic_ids = subject.setdefault("completed_topic_ids", [])
            if self.topic_id and self.topic_id not in completed_topic_ids:
                completed_topic_ids.append(self.topic_id)

            max_lessons = max(subject.get("lessons", 0), len(completed_topic_ids))
            subject["completed"] = min(len(completed_topic_ids), max_lessons)

        # Save updated progress
        out_data = {"subjects": subjects}
        with open(progress_file, "w", encoding="utf-8") as f:
            json.dump(out_data, f, indent=4)

    def load_lesson(self, subject_id, topic_id):
        """Load a lesson, resuming from last saved subtopic if available"""
        
        app = MDApp.get_running_app()
        self.current_user = app.current_user
        self.load_progress()

        self.subject_id = subject_id
        self.topic_id = topic_id

        # -------------------- Load topic metadata --------------------
        overview_path = f"data/user/{self.current_user}/subjects/{subject_id}/{subject_id}.json"
        if not os.path.exists(overview_path):
            raise FileNotFoundError(f"Overview JSON not found: {overview_path}")
        
        with open(overview_path, "r", encoding="utf-8") as f:
            overview_data = json.load(f)

        # Handle nested 'subject' structure: topics are under overview_data['subject']['topics']
        if "subject" in overview_data and isinstance(overview_data["subject"], dict):
            topics = overview_data["subject"].get("topics", [])
        else:
            # Fallback for flat structure
            topics = overview_data.get("topics", [])

        self.topic = next((t for t in topics if t["id"] == topic_id), None)
        if not self.topic:
            raise ValueError(f"Topic '{topic_id}' not found in overview JSON.")
        
        # -------------------- Create Topic Overview (Index 0) --------------------
        self.subtopics = [{
            "subtopic": self.topic["name"],
            "text": self.topic.get("description", "No description available."),
            "is_overview": True
        }]

        # -------------------- Load lesson content from <topic_id>.txt --------------------
        txt_path = f"data/user/{self.current_user}/subjects/{subject_id}/{topic_id}.txt"
        # KEEP existing overview, append real subtopics from TXT

        if os.path.exists(txt_path):
            with open(txt_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Split using new subtopic marker
            raw_subtopics = content.split('\\new_sub_topic')

            for block in raw_subtopics:
                block = block.strip()
                if not block:
                    continue

                lines = block.split("\n", 1)

                title = lines[0].strip()
                text = lines[1].strip() if len(lines) > 1 else ""

                self.subtopics.append({
                    "subtopic": title,
                    "text": text,
                    "is_overview": False
                })
        else:
            print(f"[WARNING] File not found: {txt_path}")

        '''else:
                    print(f"[WARNING] Topic index {topic_index} not found in sections")
            else:
                print(f"[WARNING] No \\newtopic found in {txt_path}")
        else:
            print(f"[WARNING] Subject TXT not found at {txt_path}")'''

        # -------------------- Resume from last saved subtopic --------------------
        self.subtopic_index = 0
        # Check if subject exists in progress and has current_subtopic
        progress_subject = next((s for s in self.user_progress.get("subjects", [])
                                if s.get("id") == self.subject_id), None)
        if progress_subject:
            saved_index = progress_subject.get("current_subtopic", 0)
            if 0 <= saved_index < len(self.subtopics):
                self.subtopic_index = saved_index

        # -------------------- Show the subtopic --------------------
        
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
        is_overview = sub.get("is_overview", False)

        if len(self.subtopics) == 1:
            self.subtopics.append({
                "subtopic": "Content Missing",
                "text": "Lesson content is unavailable.",
                "is_overview": False
            })

        # ---------- START TIMER ----------
        self.subtopic_start_time = time.time()

        # Determine typical reading time for subtopic
        if sub["text"].startswith("[") and sub["text"].endswith("]"):
            self.typical_times[self.subtopic_index] = 10  # Fixed time for diagrams
        else:
            self.typical_times[self.subtopic_index] = max(10, len(sub["text"]) // 5)

        # Set labels
        self.ids.lesson_title.text = self.topic["name"]
        if is_overview:
            self.ids.subtopic_title.text = "Overview"
        else:
            self.ids.subtopic_title.text = sub["subtopic"]

        if is_overview:
            self.ids.next_btn.text = "Begin ▶"
        else:
            self.ids.next_btn.text = "Next ▶"

        # Handle diagram or text
        if sub["text"].startswith("[") and sub["text"].endswith("]"):
            image_name = sub["text"][1:-1]
            self.ids.lesson_image.source = f"data/user/{self.current_user}/subjects/{self.subject_id}/lesson_images/{image_name}"
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
        total = len(self.subtopics) - 1
        current = max(0, self.subtopic_index)
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
        # Navigate to miniquest
        self.app.switch_to("miniquest")

    def go_tutor(self):
        """Show the embedded TutorPanel in a floating layout (half-screen)"""
        # Mark final progress first
        self.save_progress()

        # Navigate to tutor screen
        self.app.switch_to("tutor")
        

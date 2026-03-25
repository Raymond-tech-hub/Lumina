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
        self.height = 160
        self.padding = 15
        self.spacing = 10
        self.radius = [15]
        self.elevation = 5

        # --- Header with title + icon ---
        header = MDBoxLayout(orientation="horizontal", spacing=10, adaptive_height=True)
        title = MDLabel(text=topic["name"], font_style="H6", halign="left")
        
        if status == "completed":
            icon = MDIcon(icon="check-circle", theme_text_color="Custom", text_color=(0, 0.8, 0, 1))
        elif status == "locked":
            icon = MDIcon(icon="lock", theme_text_color="Custom", text_color=(0.6, 0.6, 0.6, 1))
        else:
            icon = MDIcon(icon="play-circle", theme_text_color="Custom", text_color=(0.1, 0.6, 0.9, 1))
        
        header.add_widget(title)
        header.add_widget(icon)
        self.add_widget(header)

        # --- Short description ---
        desc = MDLabel(text=topic.get("shorter_description", topic.get("short_description", "")), font_style="Body1", halign="left")
        self.add_widget(desc)

        # --- Metadata row ---
        meta_row = MDBoxLayout(orientation="horizontal", spacing=20)
        time_label = MDLabel(text=f"⏱ {topic.get('estimated_time', '?')}", font_style="Caption")
        diff_label = MDLabel(text=f"⚡ {topic.get('difficulty', '?')}", font_style="Caption")
        meta_row.add_widget(time_label)
        meta_row.add_widget(diff_label)
        self.add_widget(meta_row)

        # --- Start button ---
        if status == "next":
            btn = MDRaisedButton(text="Begin", size_hint=(None, None), size=(120, 40))
            btn.bind(on_release=lambda x: callback(topic))
            self.add_widget(btn)

class TopicRoadmapScreen(MDScreen):
    subject_id = None
    current_user = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def load_roadmap(self, subject_id):
        try:
            self.ids.roadmap_container.clear_widgets()
            app = MDApp.get_running_app()
            self.current_user = app.current_user
            self.subject_id = subject_id

            # Load user metadata
            meta_path = f"data/user/{self.current_user}/meta_data.json"
            if os.path.exists(meta_path):
                with open(meta_path, "r", encoding='utf-8') as f:
                    meta_data = json.load(f)
                    print(f"[DEBUG] Loaded meta_data.json: {meta_data.get('name', 'Unknown')}")
            else:
                print(f"[WARNING] meta_data.json not found at {meta_path}")

            # Load user progress
            user_json = f"data/user/{self.current_user}/progress/user_progress.json"
            user_data = {}
            if os.path.exists(user_json):
                with open(user_json, "r", encoding='utf-8') as f:
                    user_data = json.load(f)
            else:
                print(f"[WARNING] user_progress.json not found at {user_json}")

            subjects = user_data.get("subjects", []) if isinstance(user_data, dict) else []
            subject_progress = next((s for s in subjects if s.get("id") == subject_id), None)
            completed_count = subject_progress.get("completed", 0) if subject_progress else 0

            # Load subject topics from biology.json (nested under 'subject' key)
            overview_json = f"data/user/{self.current_user}/subjects/{subject_id}/{subject_id}.json"
            if not os.path.exists(overview_json):
                print(f"[ERROR] Subject JSON not found at {overview_json}")
                return

            with open(overview_json, "r", encoding="utf-8") as f:
                overview = json.load(f)

            # Handle nested 'subject' structure: topics are under overview['subject']['topics']
            if "subject" in overview and isinstance(overview["subject"], dict):
                subject_meta = overview["subject"]
                topics = subject_meta.get("topics", [])
                print(f"[DEBUG] Loaded subject: {subject_meta.get('name', 'Unknown')} with {len(topics)} topics")
            else:
                # Fallback for flat structure
                topics = overview.get("topics", [])
                print(f"[DEBUG] Using flat topic structure with {len(topics)} topics")

            # Resolve user placeholders in file_path
            for idx, topic in enumerate(topics):
                if "file_path" in topic:
                    topic["file_path"] = topic["file_path"].replace("<user>", str(self.current_user))
                    print(f"[DEBUG] Topic {idx}: {topic['id']} -> {topic.get('file_path', 'N/A')}")

                # Determine topic status
                if idx < completed_count:
                    status = "completed"
                elif idx == completed_count:
                    status = "next"
                else:
                    status = "locked"

                card = TopicCard(topic, status, self.start_topic)
                self.ids.roadmap_container.add_widget(card)

            print(f"[DEBUG] Loaded {len(topics)} topics for subject {subject_id}")

        except FileNotFoundError as e:
            print(f"[ERROR] File not found: {e}")
        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON decode error: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected error loading roadmap: {e}")

    def start_topic(self, topic):
        """Start the lesson using the topic info (including txt file path)."""
        app = MDApp.get_running_app()
        print(f"Starting topic: {topic['id']}")
        app.switch_to("lesson_progress")
        progress_screen = self.app.screen_manager.get_screen("lesson_progress")
        progress_screen.load_lesson(self.subject_id, topic["id"])


from kivy.clock import Clock
from kivy.animation import Animation
from kivymd.uix.screen import MDScreen


class TasksScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Example tasks
        self.tasks = [
            {
                "id": 1,
                "description": "Gain 250 XP",
                "duration_hours": 24,
                "xp": 250,
                "active": True
            },
            {
                "id": 2,
                "description": "Complete 5 quizzes",
                "duration_hours": 48,
                "xp": 500,
                "active": False
            },
        ]

        self.current_task_index = 0  # Index of the current task

    def on_enter(self, *args):
        """Called when the screen is displayed"""
        Clock.schedule_once(self._pulse_logo, 0.8)
        self.display_current_task()

    def _pulse_logo(self, dt):
        """Pulse animation for logo"""
        logo = self.ids.get('logo')
        if logo:
            anim = (Animation(opacity=0.45, duration=1.0, t='out_quad') +
                    Animation(opacity=1.0, duration=1.0, t='out_quad'))
            anim.repeat = True
            anim.start(logo)

    def display_current_task(self):
        """Update the UI for the current task"""
        task = self.tasks[self.current_task_index]
        self.ids.task_description.text = f"{task['description']} in {task['duration_hours']} hrs"

        claim_btn = self.ids.claim_button
        if task["active"]:
            claim_btn.disabled = False
            claim_btn.md_bg_color = (1, 0.85, 0, 1)  # Yellow when active
        else:
            claim_btn.disabled = True
            claim_btn.md_bg_color = (0.5, 0.5, 0.5, 1)  # Gray when inactive

    def claim_task(self):
        """Claim the current task"""
        task = self.tasks[self.current_task_index]
        if task["active"]:
            print(f"Task claimed: {task['description']}")
            # Mark task as inactive after claiming
            task["active"] = False
            self.display_current_task()

    # ================= Navigation =================
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
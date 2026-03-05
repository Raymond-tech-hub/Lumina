from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.animation import Animation
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout

from backend.ChatBot.chatbot import ChatBot
from backend.ChatBot.voice import Voice
from backend.ChatBot.token_simulation import TokenSimulation

import time

global_msg = ''

db="backend/ChatBot/Database/Bot/response.json"
fact_file="backend/ChatBot/Database/Bot/OsmosisFacts.json"

class ChatBotScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Chatbot = ChatBot(name="lumina", response_file=db, fact_file=fact_file)
        self.token_sim = TokenSimulation()
         
    def action_time(self):
        current_time = time.strftime('%H:%M:%S')
        return f"current time is: {current_time}"

    def go_back(self):
        print("entering home")
        self.manager.current = "home"

    def add_thinking_bubble(self):
        chat_container = self.ids.chat_container

        bubble_container = MDBoxLayout(
            size_hint_y=None,
            adaptive_height=True,
            padding=[dp(5), dp(5)],
        )

        bubble = MDCard(
            size_hint=(0.4, None),
            adaptive_height=True,
            padding=dp(10),
            radius=[15, 15, 15, 0],
            md_bg_color = (0, 0, 130, 1),  
            elevation=2,
        )

        bubble_label = MDLabel(
            text="Thinking...",
            adaptive_height=True,
            halign="left",
            valign="middle",
        )

        bubble.add_widget(bubble_label)

        bubble_container.add_widget(bubble)
        bubble_container.add_widget(BoxLayout())

        chat_container.add_widget(bubble_container)

        Clock.schedule_once(
            lambda x: self.ids.chat_scroll.scroll_to(bubble_container), 0.1
        )

        return bubble_container


    def add_user_message(self, text: str):
        chat_container = self.ids.chat_container

        bubble_container = MDBoxLayout(
            size_hint_y=None,
            adaptive_height=True,
            padding=[dp(5), dp(5)],
        )

        bubble = MDCard(
            size_hint=(0.75, None),  # 75% of width
            adaptive_height=True,
            padding=dp(10),
            radius=[15, 15, 0, 15],
            md_bg_color=(0.2, 0.6, 1, 1),
            elevation=2,
        )

        bubble_label = MDLabel(
            text=text,
            adaptive_height=True,
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),
            halign='left',
            valign='middle',
            text_size=(self.width * 0.7, None),  # wrap text
        )

        bubble.add_widget(bubble_label)

        # Spacer left → pushes bubble right
        bubble_container.add_widget(BoxLayout())
        bubble_container.add_widget(bubble)

        chat_container.add_widget(bubble_container)

        bubble.opacity = 0
        Animation(opacity=1, d=0.2).start(bubble)

        Clock.schedule_once(lambda x: self.ids.chat_scroll.scroll_to(bubble_container), 0.1)


    def add_bot_message(self, text: str):
        chat_container = self.ids.chat_container

        bubble_container = MDBoxLayout(
            size_hint_y=None,
            adaptive_height=True,
            padding=[dp(5), dp(5)],
        )

        bubble = MDCard(
            size_hint=(0.75, None),
            adaptive_height=True,
            padding=dp(10),
            radius=[15, 15, 15, 0],
            md_bg_color=(0.2, 0.6, 1, 1),
            elevation=2,
        )

        bubble_label = MDLabel(
            text="",
            adaptive_height=True,
            halign="left",
            valign="middle",
        )

        bubble.add_widget(bubble_label)

        # Align left
        bubble_container.add_widget(bubble)
        bubble_container.add_widget(BoxLayout())

        chat_container.add_widget(bubble_container)

        bubble.opacity = 0
        Animation(opacity=1, d=0.2).start(bubble)

        Clock.schedule_once(
            lambda x: self.ids.chat_scroll.scroll_to(bubble_container), 0.1
        )

        # 🔥 Start streaming text
        self.token_sim.ui_text(bubble_label, text)



    def send_message(self):
        msg = self.ids.user_input.text.strip()
        if not msg:
            return

        self.add_user_message(msg)
        self.ids.user_input.text = ""

        if any(time in msg for time in ["what is the time", "current time"]):
            response =  str(self.action_time)
        else:
            response = self.Chatbot.get_response(msg)
            response = str(response)

        # 🔥 Add thinking bubble
        thinking_widget = self.add_thinking_bubble()

        # Determine delay
        length = len(response)

        if length < 15:
            delay = 1.5
        elif length < 30:
            delay = 2.2
        else:
            delay = 3.1

        # Replace thinking bubble after delay
        Clock.schedule_once(
            lambda dt: self.replace_thinking_with_response(thinking_widget, response),
            delay
        )

        self.update_recommendations(msg)

    def replace_thinking_with_response(self, thinking_widget, text):
        """
        Removes the thinking bubble and adds the real bot response.
        """
        chat_container = self.ids.chat_container
        # Remove the thinking bubble from the chat
        chat_container.remove_widget(thinking_widget)
        # Add the bot's real message
        self.add_bot_message(text)


    def update_recommendations(self, msg):
        # Example: basic keyword-based recommendations
        rec_layout = self.ids.recommendations
        rec_layout.clear_widgets()
        if "task" in msg.lower():
            buttons = ["View Tasks", "Add Task"]
        elif "reminder" in msg.lower():
            buttons = ["Set Reminder", "View Reminders"]
        else:
            buttons = ["Help", "Daily Summary"]
        for b in buttons:
            btn = MDFlatButton(text=b, on_release=lambda x, t=b: self.fill_input(t))
            rec_layout.add_widget(btn)

    def fill_input(self, text):
        self.ids.user_input.text = text

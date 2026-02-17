from kivymd.uix.screen import MDScreen

class SignupScreen(MDScreen):
    def on_enter(self):
        print("Signup screen entered")

    def try_signup(self):
        print("Signup attempt initiated")
        self.manager.current = "home"

    def switch_to_login(self):
        self.manager.current = "login"
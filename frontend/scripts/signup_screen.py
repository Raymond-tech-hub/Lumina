from kivymd.uix.screen import MDScreen
from backend.authenticaion import Authenticate

class SignupScreen(MDScreen):
    def on_enter(self):
        print("Signup screen entered")

   
    def try_signup(self):
        # --- Step 2: capture & basic validation ---
        username = self.ids.username_field.text.strip()
        full_name = self.ids.name_field.text.strip()
        email = self.ids.email_field.text.strip()
        password = self.ids.password_field.text.strip()
        confirm_password = self.ids.confirm_password.text.strip()

        missing = False
        for field_id, name in [
            ("username_field", "Username"),
            ("name_field", "Full name"),
            ("email_field", "Email"),
            ("password_field", "Password"),
            ("confirm_password", "Confirm password")
        ]:
            if not getattr(self.ids, field_id).text.strip():
                getattr(self.ids, field_id).error = True
                getattr(self.ids, field_id).helper_text = f"{name} is required"
                missing = True
        if missing:
            return

        if password != confirm_password:
            self.ids.confirm_password.error = True
            self.ids.confirm_password.helper_text = "Passwords do not match"
            return

        # --- Step 3: Insert into authentication DB ---
        folder = "data/user"
        database_file = "auth.db"
        auth = Authenticate(folder=folder, db=database_file)

        # Attempt insertion
        success = auth.insert_data(
            username=username,
            name=full_name,
            email=email,
            password=password
        )

        if not success:
            # If insertion failed due to unique constraints, catch and show helper_text
            # SQLite error message includes 'UNIQUE constraint failed'
            # For simplicity, we'll check email and username separately
            auth.c.execute("SELECT 1 FROM users WHERE username = ?", (username,))
            if auth.c.fetchone():
                self.ids.username_field.error = True
                self.ids.username_field.helper_text = "Username already exists"

            auth.c.execute("SELECT 1 FROM users WHERE email = ?", (email,))
            if auth.c.fetchone():
                self.ids.email_field.error = True
                self.ids.email_field.helper_text = "Email already exists"

            return

        # At this point, insertion succeeded
        print("User registered successfully!")
        # Next: Step 4 will be creating the user's folder structure using user_id
        # Step 4a: Get the new user_id
        auth.c.execute("SELECT id FROM users WHERE email = ?", (email,))
        row = auth.c.fetchone()
        if not row:
            print("Error: user ID not found after insertion")
            return
        user_id = row[0]

        # Step 4b: Build the folder structure
        from backend.user_builder import LuminaUserBuilder  # assuming you saved the class here
        builder = LuminaUserBuilder(base_path="data/user")
        builder.build_user(user_id)

        print(f"Folder structure created for user ID {user_id}")

        # Step 4c: Optionally, switch to home screen
        app = MDApp.get_running_app()
        app.load_user_graphs(user_id)  # sets current_user and loads data
        self.manager.current = "home"


    def switch_to_login(self):
        self.manager.current = "login"
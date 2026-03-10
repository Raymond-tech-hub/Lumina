import os
import json

class UserBuilder:
    """
    Class to build folder structure and JSON files for a Lumina user.
    Does not touch existing images.
    """
    
    def __init__(self, base_path, learner_type):
        """
        Args:
            base_path (str): Path to the 'data/user' directory
        """
        self.base_path = base_path
        self.learner_type = learner_type
    
    def build_user(self, user_id):
        """
        Creates folder structure and JSON files for a specific user.
        
        Args:
            user_id (int or str): Unique ID for the user
        """
        user_folder = os.path.join(self.base_path, str(user_id))
        
        # Create main user folder and subfolders
        folders = [
            user_folder,
            os.path.join(user_folder, "lesson_images"),
            os.path.join(user_folder, "progress"),
            os.path.join(user_folder, "subjects")
        ]
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
        
        meta_content = {
            "id": user_id,
            "learner_type": self.learner_type,
            "subjects": ["math", "English", "computer"] #default data
}

        # JSON files to create with empty content
        json_files = {
            os.path.join(user_folder, "exam_data.json"): {},
            os.path.join(user_folder, "meta_data.json"): meta_content,
            os.path.join(user_folder, "progress", "progress.json"): {},
            os.path.join(user_folder, "progress", "user_progress.json"): {},
            os.path.join(user_folder, "subjects", "course_biology.json"): {}
        }
        
        for path, content in json_files.items():
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(content, f, indent=4)
                    print("from user_bulder: created user folder!!!!!")
        
        print(f"User {user_id} structure created successfully.")
    
    def build_multiple_users(self, user_ids, learner_type):
        """
        Builds structures for multiple users at once.
        
        Args:
            user_ids (list[int or str]): List of user IDs
        """
        for uid in user_ids:
            self.build_user(uid)



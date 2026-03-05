import os
import json

class DecisonTree:
    def __init__(self, base_path):
        self.base_path = base_path

    def choose_path(self, user_id):
        user_folder = os.path.join(self.base_path, str(user_id))
        meta_path = os.path.join(user_folder, "meta_data.json")

        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        learner_type = meta.get("learner_type", "gamer")

        print(f"User {user_id} assigned path: {learner_type}")

        return learner_type
import os
import json

class Tree:
    """Represents a user's virtual tree for gamified learning."""

    TREE_FILE = "data/user/tree_data.json"

    STAGES = [
        {"name": "Seedling 🌱", "xp_required": 0, "image": "data/user/seedling.jpeg"},
        {"name": "Sapling 🌿", "xp_required": 100, "image": "data/user/sapling.jpeg"},
        {"name": "Young Tree 🌳", "xp_required": 250, "image": "data/user/young.jpeg"},
        {"name": "Mature Tree 🌲", "xp_required": 500, "image": "data/user/tree_mature.jpeg"},
        {"name": "Grand Tree 🌴", "xp_required": 1000, "image": "data/user/grand.jpeg"}
    ]

    def __init__(self, user_id):
        self.user_id = user_id
        self.xp = 0
        self.coins = 0
        self.level = 0
        self.stage = self.STAGES[0]["name"]
        self.current_image = self.STAGES[0]["image"]

        # Expose UI-ready data directly
        self.ui_data = {
            "xp": self.xp,
            "coins": self.coins,
            "stage": self.stage,
            "current_image": self.current_image
        }

        self.load_tree()

    def update_ui_data(self):
        """Update UI-ready dict for KV binding."""
        self.ui_data = {
            "xp": self.xp,
            "coins": self.coins,
            "stage": self.stage,
            "current_image": self.current_image
        }

    def load_tree(self):
        """Load tree data from JSON if it exists."""
        uid = str(self.user_id)
        if os.path.exists(self.TREE_FILE):
            with open(self.TREE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                users_data = data.get("users", data)
                if uid in users_data:
                    user_entry = users_data[uid]
                    tree_data = user_entry.get("tree", user_entry) if isinstance(user_entry, dict) else {}
                    self.xp = tree_data.get("xp", 0)
                    self.coins = tree_data.get("coins", 0)
                    self.stage = tree_data.get("stage", self.STAGES[0]["name"])
                    self.update_stage()  # sets current_image & level
        self.update_ui_data()  # ready for KV binding


    def save_tree(self):
        uid = str(self.user_id)
        data = {}
        if os.path.exists(self.TREE_FILE):
            with open(self.TREE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

        if "users" not in data:
            if data and any(key in data for key in ["xp", "coins", "stage"]):
                data = {"users": {uid: {"tree": data}}}
            else:
                data = {"users": {k: v for k, v in data.items()}} if data else {"users": {}}

        if "users" not in data:
            data["users"] = {}

        data["users"][uid] = {
            "tree": {
                "xp": self.xp,
                "coins": self.coins,
                "stage": self.stage,
                "stages": self.STAGES
            }
        }

        parent = os.path.dirname(self.TREE_FILE)
        if parent and not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)

        with open(self.TREE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)


    def add_xp(self, amount):
        self.xp += amount
        self.update_stage()
        self.update_ui_data()
        self.save_tree()

    def add_coins(self, amount):
        self.coins += amount
        self.update_ui_data()
        self.save_tree()

    def update_stage(self):
        for i, stage in enumerate(self.STAGES):
            if self.xp >= stage["xp_required"]:
                self.level = i
                self.stage = stage["name"]
                self.current_image = stage["image"]
        self.update_ui_data()

    def get_progress(self):
        return self.ui_data

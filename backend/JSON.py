import json
import os

class MyJSON:
    def __init__(self):
        pass

    def load_json(self, json_file):
        try:
            if os.path.getsize(json_file) > 0:
                with open(json_file, "r") as f:
                    data = json.load(f)
                print(f"Successfully loaded: {json_file}")
                return data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print("Error loading json file", e)
            return None

    def create_json(self, json_file, data):
        try:
            with open(json_file, "w") as f:
                json.dump(data, f, indent=4)
            print(f"created {json_file}")
            return data
        except Exception as e:
            print("Error creating json file", e)
            return None

if __name__ == "__main__":
    j = MyJSON()
    F = j.load_json("test.json")
    if F is None:
        F = j.create_json("test.json", {"content": "Hello world! File created!"})
    print(F['content'])
    os.remove("test.json")
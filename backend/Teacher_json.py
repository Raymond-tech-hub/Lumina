from JSON import MyJSON
import os
import re

JS = MyJSON()
PATH = "data/teachers"
os.makedirs(PATH, exist_ok=True)

class Teacher:
    """Represents a teacher with ID, name, subjects, and availability."""
    
    def __init__(self, name, *subjects):
        """Initialize a Teacher instance.
        
        Args:
            name (str): The teacher's name.
            *subjects: Variable number of subject names.
        """
        self.ID = self.generate_ID(PATH)
        self.name = name
        self.subjects = list(subjects) 
        self.availability = {
            "Monday": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "Tuesday": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "Wednesday": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "Thursday": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "Friday": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        }
       
    def list_ids(self, path: str):
        """Load and extract all teacher IDs from JSON files in the given directory.
        
        Args:
            path (str): Directory path containing teacher JSON files.
            
        Returns:
            list: List of teacher IDs found in JSON files, or empty list if none exist.
        """
        try:
            files = os.listdir(path)
        except FileNotFoundError:
            return []
        ids = []
        for filename in files:
            if not filename.lower().endswith('.json'):
                continue
            filepath = os.path.join(path, filename)
            try:
                teacher = JS.load_json(filepath)
                if isinstance(teacher, dict) and 'ID' in teacher:
                    ids.append(teacher['ID'])
            except Exception:
                continue
        return ids

    def generate_ID(self, path: str) -> int:
        """Generate a unique ID for a new teacher.
        
        Args:
            path (str): Directory path containing existing teacher JSON files.
            
        Returns:
            int: New unique ID (max existing ID + 1, or 1 if none exist).
        """
        ids = self.list_ids(path)
        if not ids:
            return 1
        try:
            max_id = max(int(i) for i in ids)
        except Exception:
            max_id = max(ids)
        return max_id + 1
                                                        
    def send_to_json(self) -> dict:
        """Convert teacher data to a dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary containing ID, name, subjects, and availability.
        """
        return {
            "ID": self.ID,
            "name": self.name,
            "subjects": self.subjects,
            "availability": self.availability
        } 

    def safe_filename(self, name: str) -> str:
        """Sanitize a name to create a safe filename.
        
        Removes special characters and replaces spaces with underscores.
        
        Args:
            name (str): The input name to sanitize.
            
        Returns:
            str: A safe filename-compatible string.
        """
        name = re.sub(r'[^\w\s\-]', '', name).strip().replace(" ", "_")
        name = name.strip('_-. ')
        if not name:
            print("Name cannot be empty! using default")
            name = "Teacher"
        return name 

if __name__ == "__main__":
        
    while True:
        name = input("Enter name: ").strip()
        if name.lower() in ("exit", "quit"):
            break
        subjects_input = input("Enter subjects: ").strip()
        subjects = subjects_input.split() if subjects_input else []
        
        Tr = Teacher(name, *subjects)
        
        safe_name = Tr.safe_filename(name)  
        filename = f"{Tr.ID:02d}_{safe_name}.json" 
        
        filepath = os.path.join(PATH, filename)
        
        JS.create_json(filepath, Tr.send_to_json())
<<<<<<< HEAD
        print(f"JSON created successfully: {filename}")
=======
        print(f"JSON created successfully: {filename}")
>>>>>>> 091a002f8575af1c4c331bfd58ccabd00fe0aae0

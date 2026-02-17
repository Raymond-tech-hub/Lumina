import json
import random
import difflib

class ChatBot:
    def __init__(self, name, response_file, fact_file):
        self.name = name
        self.response_file = response_file
        self.fact_file = fact_file
        self.greetings = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "howdy", "how are you"]
        self.help = """### **1. Gamify the Learning**

* **Points and Rewards:** Give points for completing lessons, quizzes, or daily tasks. Unlock badges or cosmetic rewards.
* **Levels & Progression:** Visualize progress like a “level-up” system. Learners see improvement over time.
* **Challenges & Mini-Games:** Integrate small puzzles, timed challenges, or memory games related to the lesson content.

---

### **2. Make it Interactive**

* **Drag-and-Drop & Matching:** Replace long text exercises with interactive exercises.
* **Simulations & Scenarios:** Let learners experiment in realistic contexts (e.g., virtual labs, real-life scenarios).
* **Branching Lessons:** Depending on choices, learners follow different storylines or outcomes.
"""
        
    def load_database(self, db_file):
        database = None
        try:
            with open(db_file, "r", encoding="utf-8") as f:
                database = json.load(f)
        except Exception as e:
            print(f"Error loading data file: {db_file} > {e}")
        return database            
            
    def get_response(self, user_input):
        data = self.load_database(self.fact_file)
        best_match = None
        best_score = 0
        response = None

        if 'help' in user_input:
            return self.help

        # Iterate through each entry in the data
        for entry in data:
            for key, value in entry.items():
                queries = value.get("queries", [])
                # Find the closest match for the user input among the queries
                matches = difflib.get_close_matches(user_input, queries, n=1, cutoff=0.7)
                if matches:
                    # If we find a match, return the corresponding positive response
                    return value.get("positive", response)
                    return None
                
        db = self.load_database(self.response_file)
        if db is None:
            return "Error: Could not load response database."
            
        text = user_input.lower()
        
        # Exact substring match loop
        for key, value in db["Dialogue"].items():
            if key.lower() in text:  # Case-insensitive check
                return value
        
        # Close match check (moved outside the loop)
        possible_keys = [k.lower() for k in db["Dialogue"].keys()]  # Lowercase for better matching
        match = difflib.get_close_matches(text, possible_keys, n=1, cutoff=0.7)
        if match:
            # Find the original key (preserves original casing if needed)
            original_key = list(db["Dialogue"].keys())[possible_keys.index(match[0])]
            return db["Dialogue"][original_key]

        # Greeting check
        greeting_match = difflib.get_close_matches(text, self.greetings, n=1, cutoff=0.7)   
        if greeting_match:
            return random.choice(self.greetings).capitalize() + ", nice to meet you!"      
        
        # Final fallback
        return "Sorry! Could you rephrase that?"
                                                    
if __name__ == "__main__":
    bot = ChatBot("lumina", "Database/Bot/response.json", "Database/Bot/OsmosisFacts.json")
    while True:
        text = input("you> ")  
        response = bot.get_response(text)    
        print("Bot>", response)
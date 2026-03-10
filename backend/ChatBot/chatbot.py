import json
import random
import difflib
import time
import threading
try:
    from backend.RAG.search import VectorDatabase
except Exception as e:
    print("Error:", e)

class LLM:
    def __init__(self,
                 index_file="backend/RAG/database/vector_index.faiss",
                 sentences_file="backend/RAG/database/sentences.pt",
                 database="backend/RAG/database/training_data_intent_aware.json",
                 model="backend/RAG/model/sbert_minilm"):

        self.index_file = index_file
        self.sentences_file = sentences_file
        self.database = database
        self.model = model

        self.vd = None
        self.ready = False

        # Start background loading
        self.thread = threading.Thread(target=self._load_model, daemon=True)
        self.thread.start()

    def _load_model(self):
        try:
            print("Loading Lumina semantic engine...")

            self.vd = VectorDatabase(
                index_file=self.index_file,
                sentences_file=self.sentences_file,
                database=self.database,
                model=self.model
            )

            self.vd.load_index()

            self.ready = True
            print("Lumina semantic engine ready!")

        except Exception as e:
            print("Error loading LLM:", e)

    def search(self, query):
        if not self.ready:
            return None
        return self.vd.search(query)


class ChatBot:
    def __init__(self, name, response_file, fact_file):
        self.llm = LLM()
        #self.llm.load_index()
        self.name = name
        self.response_file = response_file
        self.fact_file = fact_file
        self.greetings = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "howdy", "how are you"]
        self.help = f"""
Welcome to Lumina 

I'm {self.name}, your AI learning guide.

My job is simple: help you understand things better.
I'll adjust explanations, examples, and challenges based on how you learn best.

Ask questions, explore ideas, and don't be afraid to make mistakes — that's how learning happens.

Let's begin your journey 
"""
        self.topics = [{
    'osmosis': (
        "DEFINITION:\n"
        "The movement of water through a semi-permeable membrane.\n\n"
        "KEY CONCEPTS:\n"
        " • Real-world examples\n"
        " • Osmotic pressure in bacteria\n"
        " • Turgor pressure in plants"
    ),
    'diffusion': (
        "DEFINITION:\n"
        "The spreading of particles from high to low concentration.\n\n"
        "KEY CONCEPTS:\n"
        " • Gas exchange in leaves\n"
        " • Nutrient absorption\n"
        " • Concentration gradients"
    )
}]
        
        self.navigation_help = '''
    Your goal is to explore, learn and nurture your curiosity,
    Lumina provides just the space you need:
        - Click the menu Icon to access lessons, settings, help center, about info and logout.
        - Click the task icon to claim your rewards after completing tasks.
        - Click the brain icon to access dailly quizes and earn xp points.
        - Click the profile icon to view your profille infomration to review and edit your personalised information.

    Good Luck!, grow and nurture your curiosity >< 
'''

        self.daily_summary = '''
    Daily Summary:
        - Learn, Explore and grow your curiosity
        - Earn XP points and grow your digital Mind
        - Gain, no matter the size - A win is a win.... Remember 'Kaizen'
'''
        
    def load_database(self, db_file):
        database = None
        try:
            with open(db_file, "r", encoding="utf-8") as f:
                database = json.load(f)
        except Exception as e:
            print(f"Error loading data file: {db_file} > {e}")
        return database            
            
    def action_time(self):
        current_time = time.strftime('%H:%M:%S')
        return f'current time is: {current_time}'

    def get_response(self, user_input):
        data = self.load_database(self.fact_file)
        best_match = None
        best_score = 0
        response = None

        if 'quick help' in user_input:
            return self.help

        elif 'daily summary' in user_input:
            return self.daily_summary

        elif 'navigation' and 'help' in user_input:
            return self.navigation_help

        elif any(t in user_input for t in [
    "can you help me with something",
    "can you help me with sth",
    "i need help with sth",
    "i need help with something"]):
            return random.choice(["Sure!, what do you need help with?",
                                   "No probs, what do you need help with?", 
                                   "Okay, what is it?"])

        elif any(t in user_input for t in [
            'can you help me with a topic',
            'i need help with a topic',
            'can you explain a topic',
            'could you explain a topic'
        ]):
            
            topic_text = "\nWhich topic would you like help with?\n"

            for entry in self.topics:
                for key, value in entry.items():
                    topic_text += f"\n{key.capitalize()}:\n{value}\n"

            return topic_text

        elif any(t in user_input for t in ["what is the time", "current time"]):
            return self.action_time()
        
        elif "who made you" in user_input:
            return "Two passianate young developers made me - Diamond; a brilliant python enthusiasts and AI tech leader & Raymond; a remarkable full-stack developer"
        
        elif "your" in user_input and "name" in user_input:
            return f"My name is {self.name} your AI Tutor in this session ready to explorer and grow with You!"

        elif 'kaizen' in user_input and any(t in user_input for t in ["explain", "what is", "what does it"]):
            return "Kaizen is a japanese word meaning: \'small improvements every day\'. It\'s not about the big wins, rather the small little things you do every day.... Keep growing!"

        # Iterate through each entry in the data
        for entry2 in data:
            for key, value in entry2.items():
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
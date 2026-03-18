import json
import os 
import random
from threading import Thread
from chatbot import ChatBot
from token_simulation import TokenSimulation
from voice import Voice

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)          
print("Working directory set to:", os.getcwd())

OsmosisFacts = "Database/Bot/OsmosisFacts.json"
ResponseFile = "Database/Bot/response.json" 

class MainLoop:
    def __init__(self, bot="Lumina", db="Database/Bot/response.json", fact_file="Database/Bot/OsmosisFacts.json"):
        self.db = db
        
        self.bot=bot
        
        self.Lumina = ChatBot(name="Lumina", fact_file=OsmosisFacts, response_file=db)

        self.model = {
            "Lumina": 0
        }
        self.model_list = [
            self.Lumina
        ]        
    
    def say(self, text):
        engine = Voice()
        return engine.speak(text)

    def main(self):
        chatbot = self.model_list[self.model[self.bot]]
        while True:
            user_input = input("You> ")
            if "quit" in user_input:
                response = random.choice(["Bye", "See you later", "Tata"])
                print("Bot>", response)
                break
            response=chatbot.get_response(user_input)   
            print(response)       
            self.say(response)

if __name__ == "__main__":
    mainloop = MainLoop()
    mainloop.main()               
                    
        
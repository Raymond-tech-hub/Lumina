import json 
import os

default_data = {
    "Dialogue": {
        "nice weather today": "Yes, the weather is beautiful today"
    }
}

response_file = "Database/Bot/response.json"

fact_file_osmosis = "Database/Bot/OsmosisFacts.json" 

def check_dir():
    directories=["Database", "Database/User", "Database/Bot"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print("Created:", directory, "✅")
        else:
            print("Directory exists ✅:", directory)            
        
def check_database(file, default):
    if not os.path.exists(response_file):
        with open(file, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=4, ensure_ascii=False)
            print("\n Created json file successfully")

    else:
        print("\n json already exists ✅")                       
def start():
    check_dir()
    check_database(response_file, default_data)   
    if os.path.exists(fact_file_osmosis):
        print("Osmosis facts exist ✅")   
start()                                      
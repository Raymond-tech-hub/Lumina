import re

class InputProcessor:
    def __init__(self):
        pass

    def basic_processor(self, text: str):
        '''
        Basic text cleaning no advanced nlp techniques used:
            param: text: str
            - Convert text to lowercase
            - Remove any punctuation
            - Tokenize - split()
        '''
        cleaned_text = re.sub(r'[\w\d]', '', text.lower())
        words = cleaned_text.split()

        return {
            'cleaned_text': cleaned_text,
            'words': words
        }
    
    def advanced_processor(self, text:str):
        '''
        Andvanced text cleaning:
            param: text: str
            _ Convert text to lowercase
            _ Remove any punctuation
            - Tokenize
        '''
        pass
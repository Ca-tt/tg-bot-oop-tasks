#
#! TODO: Hmmm, how to actually use telebot here?... 

class Bot:
    def __init__(self, name: str, language: str):
        self.name = name
        self.language = language
        self._instance = None  # Placeholder for the actual bot instance (e.g., telebot.TeleBot)
        
    def connect(self):
        print(f"{self.name} bot connected to the server!")
        
    def start(self):
        print(f"{self.name} bot started with language {self.language}!")
        
    def stop(self):
        print(f"{self.name} bot stopped!")
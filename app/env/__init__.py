"""Utilizes a singleton object to gather environment variables"""
import os
import logging 
from dotenv import load_dotenv
from app.singleton import Singleton 

class Env(Singleton):
    def __init__(self):
        load_dotenv()
        self.settings = dict(os.environ.items())

    def getenv(self, name:str):
        """Gets an environment variable from the env instance"""
        return self.settings[name]
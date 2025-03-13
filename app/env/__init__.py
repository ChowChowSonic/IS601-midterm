"""Utilizes a singleton object to gather environment variables"""
import os
import logging 
from dotenv import load_dotenv
from app.singleton import Singleton 

class Env(Singleton):
    def __init__(self):
        load_dotenv()
        self.settings = dict(os.environ.items())
        logging.info("App started")

    @staticmethod
    def getenv(name:str):
        """Gets an environment variable from the env instance"""
        return Env.get_instance().settings[name]
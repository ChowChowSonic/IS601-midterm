"""Utilizes a singleton object to gather environment variables"""
import os
import logging 
from dotenv import load_dotenv

class Env:
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__(self):
        load_dotenv()
        self.settings = dict(os.environ.items())
        logging.info("App started")

    @staticmethod
    def getenv(name:str):
        """Gets an environment variable from the env instance"""
        return Env.get_instance().settings[name]

    def get_instance(): 
        """Returns the env instance""" 
        if Env._instance is None: 
            Env._instance = Env() 
        return Env._instance

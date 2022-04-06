from json import load
from sys import modules
import os


class BaseModule:

    def __init__(self):
        self.path = modules[self.__class__.__module__].__file__
        self.variables = self.load_config()

    def load_config(self):
        directory = os.path.dirname(self.path)
        config_path = os.path.join(directory, "config.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as config:
                return load(config)

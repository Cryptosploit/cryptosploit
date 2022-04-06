from csv import DictReader
from dataclasses import dataclass
from os.path import dirname, join, exists
from sys import modules


@dataclass()
class Variable:
    value: str = ""
    description: str = ""


class Environment:
    def __init__(self):
        self.__vars = dict()

    def __str__(self):
        return str(self.__vars)

    def add_var(self, name, default_value, description):
        self.__vars[name] = Variable(default_value, description)

    def set_var(self, name, val):
        self.__vars[name].value = val

    def get_var(self, name):
        return self.__vars[name].value

    def get_description(self, name):
        return self.__vars[name].description

    def load_config(self, config_path):
        with open(config_path, newline="") as f:
            reader = DictReader(f, delimiter=",", quotechar="\"")
            for row in reader:
                self.add_var(**row)


class BaseModule:

    def __init__(self):
        self.path = modules[self.__class__.__module__].__file__
        self.env = self.load()

    def load(self):
        directory = dirname(self.path)
        config_path = join(directory, "config.csv")
        if exists(config_path):
            env = Environment()
            env.load_config(config_path)
            return env

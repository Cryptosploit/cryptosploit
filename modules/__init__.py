from csv import DictReader
from dataclasses import dataclass
from os.path import dirname, join, exists
from sys import modules

from src.exceptions import ModuleError


@dataclass()
class Variable:
    value: str = ""
    description: str = ""


class Environment:
    def __init__(self):
        self.__vars = dict()

    def get_var(self, name):
        return self.__vars[name]

    def set_var(self, name, val):
        self.__vars[name].value = val

    def load_config(self, config_path):
        with open(config_path, newline="") as f:
            reader = DictReader(f, delimiter=",", quotechar="\"")
            for row in reader:
                self.__vars[row["name"]] = Variable(row["default_value"], row["description"])


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
        raise ModuleError(f"No such file: {config_path}")

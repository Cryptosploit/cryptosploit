from csv import DictReader
from dataclasses import dataclass
from os.path import dirname, join, exists
from sys import modules
from json import dumps, JSONEncoder

from src.exceptions import ModuleError


class VariableEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


@dataclass()
class Variable:
    value: str = ""
    description: str = ""


class Environment:
    def __init__(self):
        self.__vars = dict()

    def __str__(self):
        return dumps(self.__vars, indent=4, cls=VariableEncoder)

    def get_var(self, name):
        if name in self.__vars:
            return self.__vars[name]
        print("No such variable")

    def set_var(self, name, val):
        if name in self.__vars:
            self.__vars[name].value = val
        else:
            print("No such variable")

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

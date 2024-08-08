from enum import Enum, unique
from types import DynamicClassAttribute


@unique
class BaseEnum(Enum):
    def __new__(cls, display_name, data):
        obj = object.__new__(cls)
        obj._value_ = data[0] if type(data) == tuple else data
        return obj

    def __init__(self, display_name, data):
        self._display_name = display_name
        self._data = data

    @classmethod
    def get_choices(cls):
        choice = []
        for key in cls:
            choice.append((key.val, key.display_name))
        return choice

    @classmethod
    def search_by_value(cls, value) -> 'BaseEnum':
        for key in cls:
            if str(key.val) == str(value):
                return key

    @property
    def display_name(self):
        return self._display_name

    @DynamicClassAttribute
    def val(self):
        return self._value_

    @property
    def data(self):
        return self._data

    @classmethod
    def get_ui_choices(cls):
        return [{"value": key.value, "display_name": key.display_name} for key in cls]
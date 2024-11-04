from typing import Callable
from business.weapons.interfaces import IActionStrategy
class ActionStrategy(IActionStrategy):
    def __init__(self, description: str, action_function: Callable, item_name : str):
        self.__description = description
        self.__name = item_name
        self.upgrade_function = action_function

    def do_action(self):
        self.upgrade_function()
    
    @property
    def description(self):
        return self.__description

    @property
    def name(self):
        return self.__name
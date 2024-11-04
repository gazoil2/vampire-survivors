from typing import Callable

class ActionStrategy:
    def __init__(self, description: str, action_function: Callable, item_name : str):
        self.description = description
        self.name = item_name
        self.upgrade_function = action_function

    def do_action(self):
        self.upgrade_function()
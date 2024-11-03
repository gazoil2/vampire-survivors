from typing import Callable

class ActionStrategy:
    def __init__(self, description: str, action_function: Callable):
        self.description = description
        self.upgrade_function = action_function

    def do_action(self):
        self.upgrade_function()
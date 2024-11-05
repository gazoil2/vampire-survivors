"""Module that contains custom exceptions."""


class DeadPlayerException(Exception):
    """Exception raised when the player dies."""

class LevelUpException(Exception):
    """Raised when the player levels up for the game to handle"""
    def __init__(self):
        super().__init__(f"Item  not found in inventory.")

class ExitPauseMenu(Exception):
    """Exception raised to terminate the pause menu"""
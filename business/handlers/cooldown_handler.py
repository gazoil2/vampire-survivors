"""This module contains the CooldownHandler class."""

import pygame
from business.world.ingameclock import InGameClock

class CooldownHandler:
    """A handler for cooldowns."""

    def __init__(self, cooldown_time: int):
        self.__last_action_time = InGameClock().time_elapsed
        self.__cooldown_time = cooldown_time
        

    def is_action_ready(self):
        """Check if the action is ready to be performed."""
        current_time = InGameClock().time_elapsed
        return current_time - self.__last_action_time >= self.__cooldown_time

    def put_on_cooldown(self):
        """Put the action on cooldown."""
        self.__last_action_time = InGameClock().time_elapsed
"""This module contains the InputHandler class, which handles user input for the game."""

import pygame

from business.world.game_world import GameWorld
from presentation.interfaces import IInputHandler


class InputHandler(IInputHandler):
    """Handles user input for the game."""

    def __init__(self, world: GameWorld):
        self.__world = world
        self.paused = False  
        self.__pause_key_was_down = False  

    def __get_direction(self, keys):
        x = 0
        y = 0

        if keys[pygame.K_w]:
            y -= 1

        if keys[pygame.K_s]:
            y += 1

        if keys[pygame.K_a]:
            x -= 1

        if keys[pygame.K_d]:
            x += 1

        return x, y

    def __toggle_pause(self):
        """Toggles the pause state."""
        self.paused = not self.paused
    
    def is_paused(self):
        return self.paused

    def process_input(self):
        """Processes input for movement and pause functionality."""
        keys = pygame.key.get_pressed()

        # Handle pausing
        if keys[pygame.K_p]:
            if not self.__pause_key_was_down:  # Only toggle when key is first pressed
                self.__toggle_pause()
            self.__pause_key_was_down = True
        else:
            self.__pause_key_was_down = False  # Reset when the key is released

        # Only process movement if the game is not paused
        if not self.paused:
            direction = self.__get_direction(keys)
            if direction == (0,0):
                self.__world.player.sprite.idle_sprite_update()
            else:
                self.__world.player.sprite.walking_sprite_update()
            if direction[0] == 1:
                self.__world.player.sprite.set_facing_left()
            elif direction[0] == -1:
                self.__world.player.sprite.set_facing_right()
            self.__world.player.move(direction[0], direction[1])

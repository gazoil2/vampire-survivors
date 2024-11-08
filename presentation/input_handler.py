"""This module contains the InputHandler class, which handles user input for the game."""

import pygame

from business.world.game_world import GameWorld
from presentation.interfaces import IInputHandler
from business.exceptions import PausePressed


class InputHandler(IInputHandler):
    """Handles user input for the game."""

    def __init__(self, world: GameWorld):
        self.__world = world
        self.__pause = False

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
    
    def toggle_pause(self):
        self.__pause = True
    
    def process_pause(self):
        if self.__pause:
            self.__pause = False
            raise PausePressed
    def process_input(self):
        """Processes input for movement and pause functionality."""
        keys = pygame.key.get_pressed()
        if self.__pause:
            self.__pause = False
            raise PausePressed
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

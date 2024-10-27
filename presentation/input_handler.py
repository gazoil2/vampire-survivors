"""This module contains the InputHandler class, which handles user input for the game."""

import pygame

from business.world.game_world import GameWorld
from presentation.interfaces import IInputHandler


class InputHandler(IInputHandler):
    """Handles user input for the game."""

    def __init__(self, world: GameWorld):
        self.__world = world

    def __get_direction(self, keys):
        x=0
        y=0

        if keys[pygame.K_w]:
            y-=1

        if keys[pygame.K_s]:
            y+=1

        if keys[pygame.K_a]:
            x-=1
            
        if keys[pygame.K_d]:
            x+=1

        return x,y

    def is_paused(self):
        keys = pygame.key.get_pressed()
        return keys[pygame.K_p]
    def process_input(self):
        keys = pygame.key.get_pressed()
        direction = self.__get_direction(keys)
        self.__world.player.move(direction[0],direction[1])
        self.__get_direction(keys)
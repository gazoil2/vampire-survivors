"""This module defines the Game class."""

import logging

import pygame

import settings
from business.exceptions import DeadPlayerException, LevelUpException
from business.handlers.colission_handler import CollisionHandler
from business.handlers.death_handler import DeathHandler
from business.world.interfaces import IGameWorld
from presentation.interfaces import IDisplay, IInputHandler


class Game:
    """
    Main game class.

    This is the game entrypoint.
    """

    def __init__(self, display: IDisplay, game_world: IGameWorld, input_handler: IInputHandler):
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__clock = pygame.time.Clock()
        self.__display = display
        self.__world = game_world
        self.__input_handler = input_handler
        self.__running = True
        self.__paused = True

    def __process_game_events(self):
        for event in pygame.event.get():
            # pygame.QUIT event means the user clicked X to close your window
            if event.type == pygame.QUIT:  # pylint: disable=E1101
                self.__logger.debug("QUIT event detected")
                self.__running = False

    def run(self):
        """Starts the game loop."""
        self.__logger.debug("Starting the game loop.")
        while self.__running:
            self.__paused = self.__input_handler.is_paused()
            if self.__paused:
                self.__clock.tick(settings.FPS)
                self.__input_handler.process_input()
                self.__process_game_events()
                self.__display.render_pause_screen()
                self.__display.update_display()
            else:
                try:
                    self.__clock.tick(settings.FPS)
                    self.__process_game_events()
                    self.__input_handler.process_input()
                    self.__world.update()
                    CollisionHandler.handle_collisions(self.__world)
                    DeathHandler.check_deaths(self.__world)
                    self.__display.render_frame()
                    self.__display.update_display()
                except LevelUpException:
                    self.__display.render_upgrade_screen(self.__world.player.inventory)
                    while self.__display.is_in_menu and self.__running:
                        self.__clock.tick(settings.FPS)
                        self.__process_game_events()
                        self.__display.render_upgrade_screen(self.__world.player.inventory)
                        self.__display.update_display()
                except DeadPlayerException:
                    self.__running = False

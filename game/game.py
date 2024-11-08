"""This module defines the Game class."""

import logging
import pygame
import settings
from business.world.interfaces import IGameWorld
from presentation.interfaces import IDisplay, IInputHandler
from game.gamestate import StartingState,IGameState




class Game:
    """
    Main game class.

    This is the game entrypoint.
    """

    def __init__(self, display: IDisplay, game_world: IGameWorld, input_handler: IInputHandler):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.__clock = pygame.time.Clock()
        self.display : IDisplay = display
        self.world = game_world
        self.input_handler = input_handler
        self.running = True
        self.state = StartingState()

    def __process_game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=E1101
                self.logger.debug("QUIT event detected")
                self.running = False
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE: 
                    self.input_handler.toggle_pause()

    def run(self):
        """Starts the game loop."""
        self.logger.debug("Starting the game loop.")
        while self.running:
            self.__clock.tick(settings.FPS) 
            self.__process_game_events()
            self.state.update(self)
            self.state.render(self)
    def change_state(self,new_state : IGameState):
        """Switch to a new gamestate"""
        self.state = new_state
        
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from business.exceptions import DeadPlayerException, LevelUpException, PausePressed, GameStart
from business.handlers.colission_handler import CollisionHandler
from business.handlers.death_handler import DeathHandler
from business.world.interfaces import IGameWorld
if TYPE_CHECKING:
    from game.game import Game
from presentation.interfaces import IDisplay, IInputHandler
class IGameState(ABC):

    @abstractmethod
    def update(self,game: "Game"):
        """Updates the game"""
    
    @abstractmethod
    def render(self,game: "Game"):
        """Renders the screen"""
    
class StartingState(IGameState):
    def update(self, game):
        pass

    def render(self, game):
        try:
            game.display.render_home_screen()
            game.display.update_display()
        except GameStart:
            game.change_state(RunningState())
        

class PausedState(IGameState):

    def update(self, game):
        try:
            game.input_handler.process_input()
        except PausePressed:
            game.world.player.update_stats()
            game.change_state(RunningState())

    def render(self, game):
        try:
            game.display.render_pause_screen()
            game.display.update_display()
        except PausePressed:
            game.world.player.update_stats()
            game.change_state(RunningState())

class UpgradeState(IGameState):
    def render(self, game):
        game.display.render_upgrade_screen()
        game.display.update_display()
    
    def update(self, game):
        if game.display.is_in_menu == False:
            game.world.player.update_stats()
            game.change_state(RunningState())
class GameOverState(IGameState):

    def update(self, game):
        if game.display.is_in_menu == False:
            game.change_state(RunningState())

    def render(self, game):
        game.display.render_game_over_screen()
        game.display.update_display()
    

class RunningState(IGameState):
    """State for the game running"""
    def update(self, game):
        try:
            game.input_handler.process_input()
            game.world.update()
            CollisionHandler.handle_collisions(game.world)
            DeathHandler.check_deaths(game.world)
        except LevelUpException:
            game.change_state(UpgradeState())
        except DeadPlayerException:
            game.change_state(GameOverState())
        except PausePressed:
            game.change_state(PausedState())

    def render(self, game):
        game.display.render_frame()
        game.display.update_display()

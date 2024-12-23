"""Interfaces for the presentation layer."""

from abc import ABC, abstractmethod

from business.world.interfaces import IGameWorld
from business.weapons.interfaces import IInventory


class IDisplay(ABC):
    """Interface for displaying the game world."""

    @abstractmethod
    def load_world(self, world: IGameWorld):
        """Load the world into the display.

        Args:
            world (IGameWorld): The game world to be displayed.
        """

    @abstractmethod
    def render_frame(self):
        """Render the current frame."""

    @abstractmethod
    def render_pause_screen(self):
        """Render the pause menu"""
    
    @abstractmethod
    def render_upgrade_screen(self):
       """Render the upgrade menu"""
    
    @abstractmethod
    def render_game_over_screen(self):
        """Render the game over screen"""
    
    @abstractmethod
    def render_home_screen(self):
        """Render the home screen"""

    @abstractmethod
    def update_display(self):
       """Shows the rendered frames"""
    
    
    @property
    @abstractmethod
    def is_in_menu(self):
        """Returns a bool if the display is in a menu"""

class IInputHandler(ABC):
    """Interface for handling user input."""

    @abstractmethod
    def process_input(self):
        """Process the input from the user."""
    
    @abstractmethod
    def toggle_pause(self):
        """Toggles the pause menu"""


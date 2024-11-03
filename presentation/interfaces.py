"""Interfaces for the presentation layer."""

from abc import ABC, abstractmethod

from business.world.interfaces import IGameWorld


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
    def update_display(self):
       """Shows the rendered frames"""

class IInputHandler(ABC):
    """Interface for handling user input."""

    @abstractmethod
    def process_input(self):
        """Process the input from the user."""

    @abstractmethod
    def is_paused(self):
        """Determines whether the game should be paused or not."""

from abc import ABC,abstractmethod
from typing import List
from business.entities.interfaces import IAtackShape, IUpdatable
from business.weapons.stats import ProjectileStats, PlayerStats
class IAtackShapeFactory:
    @abstractmethod
    def create_atack_shape(self, pos_x, pos_y, projectile_stats : ProjectileStats) -> IAtackShape:
        """Creates an atack"""

class IUpgradable:
    """Interface for all weapons"""

    @abstractmethod
    def upgrade():
        """Upgrades the weapon to the next level"""

    def can_be_upgraded(self) -> bool:
        """
        Determine if the item can be upgraded.

        Returns:
            bool: True if the item can be upgraded, False otherwise.
        """
        pass  # This is an abstract method, so it should not have an implementation here.

    @abstractmethod
    def get_next_level_data(self) -> dict:
        """
        Retrieve the upgrade data for the next level of the item.

        Returns:
            dict: A dictionary containing the upgrade data for the next level.

        Raises:
            InvalidLevelUp: If the item has reached its maximum level or cannot be upgraded.
        """
    @abstractmethod
    def get_unlock_info(self)-> str:
        """
        Retrieve the unlock text for this item.

        Returns:
            str: A string describing the item.

        """
class IWeapon(IUpdatable,IUpgradable):
    @property
    def name(self):
        """Returns the name of the item"""
class IPassiveItem(IUpgradable):
    @property
    def stats(self):
        """Returns the player stats modified by the passive item"""
    
    @property
    def name(self):
        """Returns the name of the item"""

class IActionStrategy:
    @abstractmethod
    def do_action(self):
        """Activates the function set as a parameter"""
    
    
    @property
    @abstractmethod
    def description(self):
        """Returns the description of the function"""
    
    @property
    @abstractmethod
    def name(self):
        """Returns the name of the action"""

class IInventory(IUpdatable, ABC):
    @abstractmethod
    def get_combined_stats(self) -> PlayerStats:
        """Returns the combined stats from all passive items in the inventory."""

    @abstractmethod
    def add_item_to_inventory(self, item: IPassiveItem | IWeapon) -> None:
        """Adds an item (weapon or passive item) to the inventory."""

    @abstractmethod
    def upgrade_item(self, item: IPassiveItem | IWeapon) -> None:
        """Upgrades an item in the inventory."""

    @abstractmethod
    def update(self, world) -> None:
        """Updates the inventory state based on the game world."""

    @abstractmethod
    def get_possible_actions(self) -> List[IActionStrategy]:
        """Returns a list of possible actions that can be performed with items in the inventory."""
    
    @abstractmethod
    def get_passives(self) -> List[IPassiveItem]:
        """Returns the list of passives the player has"""
    
    @abstractmethod
    def get_weapons(self) -> List[IWeapon]:
        """Returns the list of weapons the player has"""
    
    @property
    @abstractmethod
    def get_max_size(self) -> int:
        """Returns the max quantity of weapons or passive the inventory can have"""
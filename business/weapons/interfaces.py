from abc import ABC,abstractmethod
from business.entities.interfaces import IAtackShape, IUpdatable
from business.weapons.stats import ProjectileStats
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
class IPassiveItem(IUpgradable):
    @property
    def stats(self):
        """Returns the player stats modified by the passive item"""
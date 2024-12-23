"""This module contains interfaces for the entities in the game."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from presentation.sprite import Sprite
from business.weapons.stats import PlayerStats, MonsterStats
if TYPE_CHECKING:
    from business.weapons.interfaces import IInventory

class ISerializable:
    """Interface for persisting classes"""
    @abstractmethod
    def serialize(self) -> dict:
        """Transform the object into a dictionary"""
    
    @staticmethod
    @abstractmethod
    def deserialize(data : dict):
        """Transform the dictionary back into an object"""

class IDamageable(ABC):
    """Interface for entities that can take damage."""

    @property
    @abstractmethod
    def health(self) -> int:
        """The health of the entity.

        Returns:
            int: The health of the entity.
        """

    @abstractmethod
    def take_damage(self, amount: int):
        """Take damage.

        Args:
            amount (int): The damage an attack deals.
        """
    

class ICanDealDamage(ABC):
    """Interface for entities that can deal damage."""

    @property
    @abstractmethod
    def damage_amount(self) -> int:
        """The amount of damage the entity can deal.

        Returns:
            int: The amount of damage the entity can deal.
        """
    
    @abstractmethod
    def attack(self, damageable : IDamageable):
        """Attacks a damageable.
        
        Args:
            damageable (IDamegeable): the object that receives damage.
        """

class IUpdatable(ABC):
    """Interface for entities that can be updated."""

    @abstractmethod
    def update(self, world):
        """Update the state of the entity."""


class IHasSprite(ABC):
    """Interface for entities that have a sprite."""

    @property
    @abstractmethod
    def sprite(self) -> Sprite:
        """The sprite of the entity.

        Returns:
            Sprite: The sprite of the entity.
        """


class IHasPosition(IHasSprite):
    """Interface for entities that have a position."""

    @property
    @abstractmethod
    def pos_x(self) -> float:
        """The x-coordinate of the entity.

        Returns:
            float: The x-coordinate of the entity.
        """

    @property
    @abstractmethod
    def pos_y(self) -> float:
        """The y-coordinate of the entity.

        Returns:
            float: The y-coordinate of the entity.
        """


class ICanMove(IHasPosition):
    """Interface for entities that can move."""

    @property
    @abstractmethod
    def speed(self) -> float:
        """The speed of the entity.

        Returns:
            float: The speed of the entity.
        """

    @abstractmethod
    def move(self, direction_x: float, direction_y: float):
        """Move the entity in the given direction based on its speed.

        This method should update the entity's position and sprite.

        Args:
            direction_x (float): The direction in x-coordinate.
            direction_y (float): The direction in y-coordinate.
        """
    
    def update_position(self, new_x: float, new_y: float):
        """Directly updates the position of the entity."""


class IMonster(IUpdatable, ICanMove, IDamageable, ICanDealDamage, ISerializable):
    """Interface for monster entities."""
    @abstractmethod
    def drop_loot(self, world):
        """Function to drop loot"""
    
    @property
    @abstractmethod
    def stats(self) -> MonsterStats:
        """Returns the stats of the monster"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the name of the monster"""

class IBullet(IUpdatable, ICanMove, ICanDealDamage, IDamageable, ISerializable):
    """Interface for bullet entities."""


class IExperienceGem(IUpdatable, IHasPosition, ISerializable):
    """Interface for experience gem entities."""

    @property
    @abstractmethod
    def amount(self) -> int:
        """The amount of experience the gem gives.

        Returns:
            int: The amount of experience the gem gives.
        """


class IPlayer(IUpdatable, ICanMove, IDamageable, ICanDealDamage, ISerializable):
    """Interface for the player entity."""

    @abstractmethod
    def pickup_gem(self, gem: IExperienceGem):
        """Picks up an experience gem.

        Args:
            gem (IExperienceGem): The experience gem to pick up.
        """


    @property
    @abstractmethod
    def experience(self) -> int:
        """The experience of the player.

        Returns:
            int: The experience of the player.
        """

    @property
    @abstractmethod
    def experience_to_next_level(self) -> int:
        """The experience required to reach the next level.

        Returns:
            int: The experience required to reach the next level.
        """

    @property
    @abstractmethod
    def stats(self) -> PlayerStats:
        """The projectile stats of the player
        
        Returns:
            PlayerStats: Stats of a player
        """
    @property
    @abstractmethod
    def inventory(self) -> "IInventory":
        """The inventory of the player
        
        Returns: 
            IInventory: Inventory of the player
        """
    
    @abstractmethod
    def update_stats(self):
        """Updates the stats of the player after a level up"""
class IAtackShape(IUpdatable,IHasPosition, ISerializable):
    """Interface for the diferent shapes an atack has"""


"""Player entity module."""
import settings
from typing import Dict
from business.entities.entity import MovableEntity
from business.entities.experience_gem import ExperienceGem
from business.entities.interfaces import IDamageable, IPlayer
from presentation.sprite import PlayerSprite
from business.world.interfaces import IGameWorld
from business.weapons.stats import PlayerStats
from presentation.sprite import Sprite
from business.handlers.cooldown_handler import CooldownHandler
from business.weapons.inventory import Inventory
from business.entities.xphandler import XpHandler


class Player(MovableEntity, IPlayer):
    """Player entity.

    The player is the main character of the game. It can move around the game world and shoot at monsters.
    """


    def __init__(self, pos_x: int, pos_y: int, sprite: Sprite, inventory : Inventory, experience : int, level : int, health : int):
        super().__init__(pos_x, pos_y, 5, sprite)
        self.__health: int = health
        self.__experience_handler = XpHandler(level=level,current_xp=experience)
        self.__inventory = inventory
        self.__stats = PlayerStats.get_base_player_stats()
        self.__attacked_enemies : Dict[IDamageable,CooldownHandler] = {}
        self._logger.debug("Created %s", self)
        self.__calculate_stats()

    def __str__(self):
        return f"Player(hp={self.__health}, xp={self.experience}, lvl={self.level}, pos=({self._pos_x}, {self._pos_y}))"

    @property
    def experience(self):
        return self.__experience_handler.current_xp

    @property
    def experience_to_next_level(self):
        return self.__experience_handler.xp_to_next_level

    @property
    def damage_amount(self):
        return self.stats.armor

    @property
    def level(self):
        return self.__experience_handler.level
    @property
    def health(self) -> int:
        return self.__health
    
    @property
    def stats(self):
        return self.__stats
    
    @property
    def inventory(self):
        return self.__inventory

    def take_damage(self, amount : int):
        damage = max(amount - self.stats.armor,0)
        self.__health = max(0, self.__health - damage)
        self.sprite.take_damage()
    
    def attack(self, damageable : IDamageable):
        if damageable not in self.__attacked_enemies:
            self.__attacked_enemies[damageable] = CooldownHandler(100)
            damageable.take_damage(self.stats.armor)
        else:
            cooldown_handler = self.__attacked_enemies[damageable]
            if cooldown_handler.is_action_ready():
                damageable.take_damage(self.stats.armor)
                cooldown_handler.put_on_cooldown()

    def pickup_gem(self, gem: ExperienceGem):
        self.__gain_experience(gem.amount)
    
    def update_stats(self):
        self.__calculate_stats()

    def __calculate_stats(self):
        new_stats = PlayerStats.get_base_player_stats() + self.inventory.get_combined_stats()
        self._speed = new_stats.movement_speed
        self.__stats = new_stats
        
    def __gain_experience(self, amount: int):
        self.__experience_handler.add_xp(amount)

    def update(self, world: IGameWorld):
        super().update(world)
        
        self.__health = min(self.stats.max_health,self.__health + self.stats.recovery)
        self.__inventory.update(world)
    def serialize(self):
        return {
            "health": self.__health,
            "experience": self.experience,
            "pos_x": self._pos_x,
            "pos_y": self._pos_y,
            "level": self.level
        }

    def deserialize( data : dict):
        health = data.get("health", 100)
        experience = data.get("experience", 0)
        pos_x = data.get("pos_x", settings.WORLD_WIDTH // 2)
        pos_y = data.get("pos_y", settings.WORLD_HEIGHT // 2)
        inventory = data.get("inventory",Inventory([],[]))
        level = data.get("level",1)
        return Player(pos_x,pos_y,PlayerSprite(pos_x,pos_y),inventory,experience,level, health)
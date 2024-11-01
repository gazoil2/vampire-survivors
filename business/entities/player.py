"""Player entity module."""

import pygame
from typing import Dict
from business.entities.entity import MovableEntity
from business.entities.experience_gem import ExperienceGem
from business.entities.interfaces import ICanDealDamage, IDamageable, IPlayer
from business.world.interfaces import IGameWorld
from business.weapons.stats import PlayerStats
from presentation.sprite import Sprite
from business.handlers.cooldown_handler import CooldownHandler
from business.weapons.interfaces import IWeapon


class Player(MovableEntity, IPlayer, IDamageable, ICanDealDamage):
    """Player entity.

    The player is the main character of the game. It can move around the game world and shoot at monsters.
    """


    def __init__(self, pos_x: int, pos_y: int, sprite: Sprite, initial_stats : PlayerStats ):
        super().__init__(pos_x, pos_y, 5, sprite)
        self.__health: int = 100
        self.__experience = 0
        self.__experience_to_next_level = 1
        self.__level = 1
        self.__weapon = None
        self.__stats = initial_stats
        self.__attacked_enemies : Dict[IDamageable,CooldownHandler] = {}
        self._logger.debug("Created %s", self)

    def __str__(self):
        return f"Player(hp={self.__health}, xp={self.__experience}, lvl={self.__level}, pos=({self._pos_x}, {self._pos_y}))"

    @property
    def experience(self):
        return self.__experience

    @property
    def experience_to_next_level(self):
        return self.__experience_to_next_level

    @property
    def level(self):
        return self.__level

    @property
    def damage_amount(self):
        return self.stats.armor

    @property
    def health(self) -> int:
        return self.__health

    def take_damage(self, amount : int):
        self.__health = max(0, self.__health - amount)
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
    
    def set_weapon(self, weapon : IWeapon):
        self.__weapon = weapon

    def __gain_experience(self, amount: int):
        self.__experience += amount
        if self.__experience >= self.__experience_to_next_level:
            self.__experience = 0
            self.__level += 1
            self.__experience_to_next_level = self.__experience_to_next_level * 2
            if self.__weapon != None:
                self.__weapon.upgrade()

    @property
    def stats(self):
        return self.__stats


    def update(self, world: IGameWorld):
        super().update(world)
        if self.__weapon != None:
            self.__weapon.update(world)
        
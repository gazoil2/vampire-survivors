"""Player entity module."""

import pygame

from business.handlers.cooldown_handler import CooldownHandler
from business.entities.bullet import Bullet
from business.entities.entity import MovableEntity
from business.entities.experience_gem import ExperienceGem
from business.entities.interfaces import ICanDealDamage, IDamageable, IPlayer
from business.world.interfaces import IGameWorld
from presentation.sprite import Sprite
from business.weapons.interfaces import IWeapon


class Player(MovableEntity, IPlayer, IDamageable, ICanDealDamage):
    """Player entity.

    The player is the main character of the game. It can move around the game world and shoot at monsters.
    """

    BASE_DAMAGE = 5

    def __init__(self, pos_x: int, pos_y: int, sprite: Sprite):
        super().__init__(pos_x, pos_y, 5, sprite)
        self.__health: int = 100
        self.__experience = 0
        self.__experience_to_next_level = 1
        self.__level = 1
        self.__weapon = None
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
        return Player.BASE_DAMAGE

    @property
    def health(self) -> int:
        return self.__health

    def take_damage(self, amount):
        self.__health = max(0, self.__health - amount)
        self.sprite.take_damage()

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

    #def __shoot_at_nearest_enemy(self, world: IGameWorld):
        
        
     #    if not world.monsters:
     #        return  # No monsters to shoot at
        

        # Find the nearest monster
 #        monster = min(
  #           world.monsters,
   #          key=lambda monster: (
   #              (monster.pos_x - self.pos_x) ** 2 + (monster.pos_y - self.pos_y) ** 2
   #          ),
   #      )
        
        #print("SHOOTOOTOTOO")
        # Create a bullet towards the nearest monster
     #    bullet = Bullet(self.pos_x, self.pos_y, monster.pos_x, monster.pos_y, 10)
    #     world.add_bullet(bullet)


    def update(self, world: IGameWorld):
        super().update(world)
        if self.__weapon != None:
            self.__weapon.update(world)
        
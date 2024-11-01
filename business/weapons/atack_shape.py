from typing import List, Dict
from random import choice
from business.entities.interfaces import IBullet, IMonster
from business.entities.entity import MovableEntity
from business.world.interfaces import IGameWorld
from business.weapons.stats import ProjectileStats
from business.handlers.cooldown_handler import CooldownHandler
from business.entities.interfaces import IDamageable
from presentation.sprite import Sprite

class NormalBullet(MovableEntity,IBullet):
    """Atack that chooses the nearest enemy"""
    def __init__(self,pos_x: float, pos_y: float,sprite : Sprite, projectile_stats: ProjectileStats):
        self.__stats = projectile_stats
        new_velocity = self.__stats.velocity
        super().__init__(pos_x,pos_y,new_velocity,sprite)
        sprite.scale_image(self.__stats.area_of_effect)
        self.__direction = (0,0)
        self.__pierce = self.__stats.pierce
        self.__attacked_enemies = []
        self.__has_set_direction = False

    @property
    def damage_amount(self):
        return self.__stats.damage

    def __set_direction(self, monsters : List[IMonster]):
        if not monsters:
            raise ValueError("No hay monstruos para atacar")
        nearest_monster = min(monsters, key=lambda monster: self._get_distance_to(monster))
        self.__direction = self._get_direction_to(nearest_monster.pos_x, nearest_monster.pos_y)
        self.__has_set_direction = True
    
    def update(self, world : IGameWorld):
        if not self.__has_set_direction:
            try:
                self.__set_direction(world.monsters)
            except ValueError:
                world.remove_bullet(self)
        self.move(self.__direction[0],self.__direction[1])
        super().update(world)
    
    @property
    def health(self) -> int:
        return self.__pierce
        
    def take_damage(self, _ : int):
        pass
    
    def attack(self, damageable : IDamageable):
        if damageable not in self.__attacked_enemies:
            damageable.take_damage(self.__stats.damage)
            self.__attacked_enemies.append(damageable)
            self.__pierce -= 1

    def __str__(self) -> str:
        return f"NormalBullet at position ({self._pos_x}, {self._pos_y})"

import random

class RandomBullet(NormalBullet):
    def __init__(self, pos_x: float, pos_y: float, sprite: Sprite, projectile_stats: ProjectileStats):
        super().__init__(pos_x, pos_y, sprite, projectile_stats)

    def __set_direction(self, monsters: List[IMonster]):
        if not monsters:
            raise ValueError("No hay monstruos para atacar")
        self.__has_set_direction = True
        # Use random.choice to select a random monster
        random_monster = random.choice(monsters)
        self.__direction = self._get_direction_to(random_monster.pos_x, random_monster.pos_y)

    def update(self, world: IGameWorld):
        super().update(world)
    
    def take_damage(self, _: int):
        pass

    def attack(self, damageable: IDamageable):
        return super().attack(damageable)

    @property
    def damage_amount(self):
        return self.__stats.damage
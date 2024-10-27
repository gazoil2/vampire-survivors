from typing import List, Dict
from business.entities.interfaces import IBullet, IMonster
from business.entities.entity import MovableEntity
from business.world.interfaces import IGameWorld
from business.weapons.stats import ProjectileStats
from business.handlers.cooldown_handler import CooldownHandler
from business.entities.interfaces import IDamageable
from presentation.sprite import Sprite

class NormalBullet(MovableEntity,IBullet):
    """Atack that chooses the nearest enemy"""
    BULLET_SPEED = 5
    BASE_PIERCE = 2
    BASE_DAMAGE = 5
    def __init__(self,pos_x: float, pos_y: float,sprite : Sprite, projectile_stats: ProjectileStats):
        self.__stats = projectile_stats
        new_velocity = self.BULLET_SPEED * (self.__stats.velocity / 100)
        super().__init__(pos_x,pos_y,new_velocity,sprite)
        sprite.scale_image(self.__stats.area_of_effect / 100)
        self.__direction = (0,0)
        self.__pierce = self.BASE_PIERCE
        self.__attacked_enemies = []
        self.__has_set_direction = False

    @property
    def damage_amount(self):
        return self.BASE_DAMAGE * (self.__stats.power / 100)

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
            damageable.take_damage(self.BASE_DAMAGE)
            self.__attacked_enemies.append(damageable)
            self.__pierce -= 1

    def __str__(self) -> str:
        return f"NormalBullet at position ({self._pos_x}, {self._pos_y})"
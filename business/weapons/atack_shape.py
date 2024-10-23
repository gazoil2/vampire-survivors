from typing import List
from business.entities.interfaces import IBullet, IMonster
from business.entities.entity import MovableEntity
from business.world.interfaces import IGameWorld
from presentation.sprite import Sprite

class NormalBullet(MovableEntity,IBullet):
    """Atack that chooses the nearest enemy"""
    BULLET_SPEED = 5
    BASE_PIERCE = 2
    def __init__(self,pos_x: float, pos_y: float,sprite : Sprite, Stats):
        super().__init__(pos_x,pos_y,self.BULLET_SPEED,sprite)
        self.__direction = (0,0)
        self.__pierce = self.BASE_PIERCE
        self.__has_set_direction = False

    @property
    def damage_amount(self):
        return 5

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
        
    def take_damage(self, _: int):
        self.__pierce -= 1
    
    def __str__(self) -> str:
        return f"NormalBullet at position ({self._pos_x}, {self._pos_y})"
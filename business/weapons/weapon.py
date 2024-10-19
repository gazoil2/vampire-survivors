from business.weapons.stats import IPlayerStats
from business.weapons.interfaces import IAtackShapeFactory, IWeapon
from business.weapons.atack_shape import NormalBullet
from business.handlers.cooldown_handler import CooldownHandler
from business.world.game_world import IGameWorld
class Weapon(IWeapon):
    def __init__(self, base_damage : int, base_cooldown : int, atack_shape : IAtackShapeFactory):
        self.__base_cooldown = base_cooldown
        self.__base_damage = base_damage
        self.__cooldown_handler = CooldownHandler(base_cooldown)
        self.__atack_shape = atack_shape

    def __shoot(self, world : IGameWorld):
        bullet = self.__atack_shape.create_atack_shape(world.player.pos_x,world.player.pos_y)
        world.add_bullet(bullet)
    
    def update(self, world : IGameWorld):
        if self.__cooldown_handler.is_action_ready():
            self.__shoot(world)
            self.__cooldown_handler.put_on_cooldown()
        super().update(world)
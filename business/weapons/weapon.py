from business.weapons.stats import ProjectileStats
from business.weapons.interfaces import IAtackShapeFactory, IWeapon
from business.weapons.atack_shape import NormalBullet
from business.handlers.cooldown_handler import CooldownHandler
from business.world.game_world import IGameWorld
class Weapon(IWeapon):
    def __init__(self, stats : ProjectileStats, atack_shape : IAtackShapeFactory):
        self.__cooldown_handler = CooldownHandler(stats.reload_time)
        self.__atack_shape = atack_shape
        self.__stats = stats

    def __shoot(self, world : IGameWorld):
        bullet = self.__atack_shape.create_atack_shape(world.player.pos_x,world.player.pos_y, self.__stats + world.player.stats)
        world.add_bullet(bullet)
    
    def update(self, world : IGameWorld):
        if self.__cooldown_handler.is_action_ready():
            self.__shoot(world)
            self.__cooldown_handler.put_on_cooldown()
        super().update(world)
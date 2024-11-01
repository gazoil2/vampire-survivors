from business.weapons.stats import ProjectileStatsMultiplier, ProjectileStats
from business.weapons.interfaces import IAtackShapeFactory, IWeapon
from business.weapons.atack_shape import NormalBullet
from business.handlers.cooldown_handler import CooldownHandler
from business.world.game_world import IGameWorld
from business.weapons.upgrade import Upgrade

class Weapon(IWeapon):
    def __init__(self, projectile_stats: ProjectileStats, atack_shape: IAtackShapeFactory, json_file: str,name : str ,weapon_level: int = 1):
        self.__cooldown_handler = CooldownHandler(projectile_stats.reload_time)
        self.__atack_shape = atack_shape
        self.__stats = projectile_stats
        self.__upgrade = Upgrade(name, json_file) 
        self.__weapon_level = weapon_level

    def __shoot(self, world: IGameWorld):
        new_stats = self.__stats * world.player.stats.projectile_stats
        self.__cooldown_handler = CooldownHandler(new_stats.reload_time)
        bullet = self.__atack_shape.create_atack_shape(world.player.pos_x, world.player.pos_y, new_stats)
        world.add_bullet(bullet)

    def upgrade(self):
        self.__weapon_level += 1
        self.__stats = self.__upgrade.apply_upgrade(self.__weapon_level, self.__stats)

    def update(self, world: IGameWorld):
        if self.__cooldown_handler.is_action_ready():
            self.__shoot(world)
            self.__cooldown_handler.put_on_cooldown()
        super().update(world)

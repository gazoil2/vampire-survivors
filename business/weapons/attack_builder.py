from business.weapons.interfaces import IAtackShapeFactory
from business.weapons.atack_shape import NormalBullet,RandomBullet
from business.weapons.stats import ProjectileStatsMultiplier
import settings
from presentation.sprite import CircleBullet

class GreenBulletFactory(IAtackShapeFactory):

    def create_atack_shape(self, player_pos_x,player_pos_y, projectile_stats) -> NormalBullet:
        return NormalBullet(player_pos_x, player_pos_y, CircleBullet(player_pos_x,player_pos_y,5,(0,255,0)), projectile_stats)


class RedBulletFactory(IAtackShapeFactory):
    def create_atack_shape(self, player_pos_x,player_pos_y, projectile_stats) -> RandomBullet:
        return RandomBullet(player_pos_x, player_pos_y, CircleBullet(player_pos_x,player_pos_y), projectile_stats)

class BigBulletFactory(IAtackShapeFactory): 
    def create_atack_shape(self, player_pos_x,player_pos_y, projectile_stats) -> NormalBullet:
        return NormalBullet(player_pos_x, player_pos_y, CircleBullet(player_pos_x,player_pos_y, 15, (245,179,66)), projectile_stats)

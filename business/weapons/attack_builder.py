import math
from typing import List
from business.weapons.interfaces import IAtackShapeFactory
from business.weapons.atack_shape import NormalBullet,RandomBullet, RotatingBullet, TrailBullet
from business.weapons.stats import ProjectileStats
import settings
from presentation.sprite import CircleBullet, ImageSprite

class GreenBulletFactory(IAtackShapeFactory):

    def create_atack_shape(self, player_pos_x,player_pos_y, projectile_stats: ProjectileStats) -> NormalBullet:
        return NormalBullet(player_pos_x, player_pos_y, ImageSprite(player_pos_x,player_pos_y,"./assets/bullets/greenbullet.png"), projectile_stats)

class RedBulletFactory(IAtackShapeFactory):
    def create_atack_shape(self, player_pos_x,player_pos_y, projectile_stats: ProjectileStats) -> RandomBullet:
        return RandomBullet(player_pos_x, player_pos_y, ImageSprite(player_pos_x,player_pos_y, "./assets/bullets/redbullet.png"), projectile_stats)

class BigBulletFactory(IAtackShapeFactory): 
    def create_atack_shape(self, player_pos_x,player_pos_y, projectile_stats : ProjectileStats) -> NormalBullet:
        return NormalBullet(player_pos_x, player_pos_y, ImageSprite(player_pos_x,player_pos_y, "./assets/bullets/bigbullet.png"), projectile_stats)

class CircularProjectileAttackFactory(IAtackShapeFactory):
    def create_atack_shape(self, player_pos_x: float, player_pos_y: float, projectile_stats: ProjectileStats) -> List[RotatingBullet]:
        return RotatingBullet(player_pos_x, player_pos_y, ImageSprite(player_pos_x,player_pos_y,"./assets/bullets/bible.png"), projectile_stats)

class TrailBulletFactory(IAtackShapeFactory):
    def create_atack_shape(self, player_pos_x: float, player_pos_y: float, projectile_stats: ProjectileStats) -> TrailBullet:
        return TrailBullet(player_pos_x, player_pos_y, ImageSprite(player_pos_x, player_pos_y, "./assets/bullets/trail.png"), projectile_stats)

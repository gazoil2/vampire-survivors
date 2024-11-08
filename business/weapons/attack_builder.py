import math
from typing import List
from business.weapons.interfaces import IAtackShapeFactory
from business.weapons.attack_shape import NormalBullet,RandomBullet, RotatingBullet, SantaWaterBullet
from business.weapons.stats import ProjectileStats
import settings
from presentation.sprite import CircleBullet, ImageSprite

class BulletFactory:
    """Factory class to create different types of bullet factories based on names."""
    
    @staticmethod
    def get_factory_by_name(name: str) -> IAtackShapeFactory:
        """Return the appropriate bullet factory based on the given name."""
        if name == "Normalbullet":
            return GreenBulletFactory()
        elif name == "RandomBullet":
            return RedBulletFactory()
        elif name == "Bigbullet":
            return BigBulletFactory()
        elif name == "Rotatingbullet":
            return CircularProjectileAttackFactory()
        elif name == "Trailbullet":
            return TrailBulletFactory()
        else:
            raise ValueError(f"Unknown bullet factory name: {name}")

class GreenBulletFactory(IAtackShapeFactory):
    def create_atack_shape(self, player_pos_x,player_pos_y, projectile_stats: ProjectileStats) -> NormalBullet:
        return NormalBullet(player_pos_x, player_pos_y, ImageSprite(player_pos_x,player_pos_y,"./assets/bullets/greenbullet.png"), projectile_stats)

class RedBulletFactory(IAtackShapeFactory):
    def create_atack_shape(self, player_pos_x,player_pos_y, projectile_stats: ProjectileStats) -> RandomBullet:
        return RandomBullet(player_pos_x, player_pos_y, ImageSprite(player_pos_x,player_pos_y, "./assets/bullets/redbullet.png"), projectile_stats)

class BigBulletFactory(IAtackShapeFactory): 
    def create_atack_shape(self, player_pos_x,player_pos_y, projectile_stats : ProjectileStats) -> NormalBullet:
        return NormalBullet(player_pos_x, player_pos_y, ImageSprite(player_pos_x,player_pos_y, "./assets/bullets/bigbullet.png"), projectile_stats, "Bigbullet")

class CircularProjectileAttackFactory(IAtackShapeFactory):
    def create_atack_shape(self, player_pos_x: float, player_pos_y: float, projectile_stats: ProjectileStats) -> List[RotatingBullet]:
        return RotatingBullet(player_pos_x, player_pos_y, ImageSprite(player_pos_x,player_pos_y,"./assets/bullets/bible.png"), projectile_stats)

class TrailBulletFactory(IAtackShapeFactory):
    def create_atack_shape(self, player_pos_x: float, player_pos_y: float, projectile_stats: ProjectileStats) -> SantaWaterBullet:
        return SantaWaterBullet(player_pos_x, player_pos_y, ImageSprite(player_pos_x, player_pos_y, "./assets/bullets/trail.png"), projectile_stats)

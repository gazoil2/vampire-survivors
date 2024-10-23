from business.weapons.interfaces import IAtackShapeFactory
from business.weapons.atack_shape import NormalBullet
from business.weapons.stats import ProjectileStats
import settings
from presentation.sprite import GreenCircleBullet

class NormalBulletFactory(IAtackShapeFactory):
    def __init__(self, speed: float):
        self.speed = speed
        self.pos_x = settings.SCREEN_WIDTH // 2
        self.pos_y = settings.SCREEN_HEIGHT // 2
    
    def create_atack_shape(self, player_pos_x,player_pos_y) -> NormalBullet:
        return NormalBullet(player_pos_x, player_pos_y, GreenCircleBullet(self.pos_x,self.pos_y))

from business.weapons.weapon import Weapon
from business.weapons.stats import ProjectileStats
from business.weapons.attack_builder import GreenBulletFactory,RedBulletFactory, BigBulletFactory, CircularProjectileAttackFactory
class WeaponFactory:
    
    @staticmethod
    def get_green_wand():
        return Weapon(ProjectileStats.get_base_stats(),GreenBulletFactory(), "Green Wand")
    
    @staticmethod
    def get_red_wand():
        return Weapon(ProjectileStats.get_base_stats(),RedBulletFactory(), "Red Wand")

    @staticmethod
    def get_shotgun():
        return Weapon(ProjectileStats(50, 3, 1, 3000, 10, 500 ), BigBulletFactory(), "Shotgun") 
    
    @staticmethod
    def get_bible():
        return Weapon(ProjectileStats(1,20,1,400,100,2000),CircularProjectileAttackFactory(), "Bible" )
    
    @staticmethod
    def get_all_weapons():
        return [WeaponFactory.get_bible(),WeaponFactory.get_green_wand(),WeaponFactory.get_red_wand(),WeaponFactory.get_shotgun()]
from business.weapons.weapon import Weapon
from business.weapons.stats import ProjectileStats
from business.weapons.attack_builder import GreenBulletFactory,RedBulletFactory, BigBulletFactory, CircularProjectileAttackFactory
class WeaponFactory:
    @staticmethod
    def get_green_wand():
        return Weapon(ProjectileStats.get_base_stats(),GreenBulletFactory(), "data/upgrades/upgrade.json", "greenwand")
    
    @staticmethod
    def get_red_wand():
        return Weapon(ProjectileStats.get_base_stats(),RedBulletFactory(), "data/upgrades/upgrade.json", "redwand")

    @staticmethod
    def get_shotgun():
        return Weapon(ProjectileStats(50, 3, 1, 3000, 10, 500 ), BigBulletFactory(), "data/upgrades/upgrade.json", "redwand") 
    
    @staticmethod
    def get_bible():
        return Weapon(ProjectileStats(1,20,1,400,100,2000),CircularProjectileAttackFactory(), "data/upgrades/upgrade.json", "redwand" )
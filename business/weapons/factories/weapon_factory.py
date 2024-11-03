from business.weapons.weapon import Weapon
from business.weapons.stats import ProjectileStats
from business.weapons.attack_builder import GreenBulletFactory,RedBulletFactory, BigBulletFactory, CircularProjectileAttackFactory, TrailBulletFactory
class WeaponFactory:
    
    @staticmethod
    def get_green_wand():
        return Weapon( ProjectileStats(damage=5, velocity=5, area_of_effect=1, reload_time=300, pierce=1,duration= 1000),GreenBulletFactory(), "Green Wand")
    
    @staticmethod
    def get_red_wand():
        return Weapon( ProjectileStats(damage=10, velocity=5, area_of_effect=1.5, reload_time=300, pierce=2, duration=1000),RedBulletFactory(), "Red Wand")

    @staticmethod
    def get_shotgun():
        return Weapon(ProjectileStats(damage=20, velocity=3, area_of_effect=3, reload_time=3000, pierce=10, duration=500 ), BigBulletFactory(), "Shotgun") 
    
    @staticmethod
    def get_bible():
        return Weapon(ProjectileStats(damage=4,velocity=20,area_of_effect=1,reload_time=400,pierce=100,duration=2000),CircularProjectileAttackFactory(), "Bible" )
    
    @staticmethod
    def get_spectral_wand():
        return Weapon(ProjectileStats(damage=2, velocity=0, area_of_effect=0.5, reload_time=45, pierce=80, duration=1500), TrailBulletFactory(), "Goo Wand")

    @staticmethod
    def get_all_weapons():
        return [
            WeaponFactory.get_bible(),
            WeaponFactory.get_green_wand(),
            WeaponFactory.get_red_wand(),
            WeaponFactory.get_shotgun(),
            WeaponFactory.get_spectral_wand()  # Add the new weapon to the list
        ]
from business.weapons.weapon import Weapon
from business.weapons.interfaces import IWeapon
from business.weapons.stats import ProjectileStats
from business.weapons.attack_builder import GreenBulletFactory,RedBulletFactory, BigBulletFactory, CircularProjectileAttackFactory, TrailBulletFactory
class WeaponFactory:
    
    @staticmethod
    def get_green_wand() -> IWeapon:
        return Weapon( ProjectileStats(damage=5, velocity=5, area_of_effect=1, reload_time=500, pierce=1,duration= 1000),GreenBulletFactory(), "Green Wand")
    
    @staticmethod
    def get_red_wand() -> IWeapon:
        return Weapon( ProjectileStats(damage=10, velocity=5, area_of_effect=1.5, reload_time=300, pierce=2, duration=1000),RedBulletFactory(), "Red Wand")

    @staticmethod
    def get_big_bow() -> IWeapon:
        return Weapon(ProjectileStats(damage=20, velocity=3, area_of_effect=3, reload_time=3000, pierce=10, duration=500 ), BigBulletFactory(), "Big Bow") 
    
    @staticmethod
    def get_bible() -> IWeapon:
        return Weapon(ProjectileStats(damage=4,velocity=20,area_of_effect=1,reload_time=400,pierce=100,duration=2000),CircularProjectileAttackFactory(), "Bible" )
    
    @staticmethod
    def get_spectral_wand() -> IWeapon:
        return Weapon(ProjectileStats(damage=2, velocity=0, area_of_effect=6, reload_time=700, pierce=80, duration=300), TrailBulletFactory(), "Spectral Wand")

    @staticmethod
    def get_weapon_by_name(name,level):
        weapon = None
        if name == "Green Wand":
            weapon = WeaponFactory.get_green_wand()
        elif name == "Red Wand":
            weapon = WeaponFactory.get_red_wand()
        elif name == "Big Bow":
            weapon = WeaponFactory.get_big_bow()
        elif name == "Bible":
            weapon = WeaponFactory.get_bible()
        elif name == "Spectral Wand":
            weapon = WeaponFactory.get_spectral_wand()
        for _ in range(level - 1):
            weapon.upgrade()
        
        return weapon

    @staticmethod
    def get_all_weapons():
        return [
            WeaponFactory.get_bible(),
            WeaponFactory.get_green_wand(),
            WeaponFactory.get_red_wand(),
            WeaponFactory.get_big_bow(),
            WeaponFactory.get_spectral_wand()  # Add the new weapon to the list
        ]
from typing import List
from business.weapons.stats import ProjectileStatsMultiplier
from business.weapons.interfaces import IUpdatable, IUpgradable, PassiveItems
class Inventory(IUpdatable):
    def __init__(self, weapons : List[IUpgradable], boosters : List[PassiveItems], maxsize=5 ) -> None:
        self.__weapons = weapons
        self.__passive_items = boosters
        self.__maxsize = maxsize

    def get_combined_stats(self):
        final_stats = ProjectileStatsMultiplier.get_empty_projectile_stats()
        for passive in self.__passive_items:
            final_stats += passive.stats 
        
        return final_stats

    def update(self, world):
        for weapon in self.__weapons:
            weapon.update(world)
    
    
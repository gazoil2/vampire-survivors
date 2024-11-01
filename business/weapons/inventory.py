from business.weapons.stats import ProjectileStatsMultiplier
class Inventory:
    def __init__(self, items, boosters, maxsize=5 ) -> None:
        self.__items = items
        self.__passive_items = boosters
        self.__maxsize = maxsize
        

    def get_combined_stats(self):
        final_stats = ProjectileStatsMultiplier.get_empty_projectile_stats()
        for passive in self.__passive_items:
            final_stats += passive.stats 
        
        return final_stats
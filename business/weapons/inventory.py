from business.weapons.stats import ProjectileStats
class Inventory:
    def __init__(self,items, boosters) -> None:
        self.__items = items
        self.__passive_items = boosters
        

    def get_combined_stats(self):
        final_stats = ProjectileStats(0,0,0,0,0)
        for booster in self.__passive_items:
            final_stats += booster.stats 
        
        return final_stats
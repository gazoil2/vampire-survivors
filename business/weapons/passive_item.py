from business.weapons.stats import PlayerStats
from business.weapons.upgrade import Upgrade
class PassiveItem:
    def __init__(self, name : str ,player_stats : PlayerStats, json_file: str, weapon_level: int = 1) -> None:
        self.__name = name
        self.__level = weapon_level
        self.__upgrades = Upgrade(name,json_file)
        self.__stats = player_stats
    
    def upgrade(self):
        self.__stats = self.__upgrades.apply_upgrade(self.__level,self.__stats)
    
    @property
    def stats(self):
        return self.__stats
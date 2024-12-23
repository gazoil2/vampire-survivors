from business.weapons.stats import PlayerStats
from business.weapons.upgrade import Upgrade
from business.weapons.interfaces import IPassiveItem
class PassiveItem(IPassiveItem):
    def __init__(self, name : str, weapon_level: int = 1) -> None:
        self.__name = name
        self.__level = weapon_level
        self.__upgrade = Upgrade(name)
        self.__stats = PlayerStats.get_empty_player_stats()
        for _ in range(weapon_level):
            self.__upgrade.apply_upgrade(self.__level,self.__stats)

    
    def upgrade(self):
        self.__level += 1
        self.__stats = self.__upgrade.apply_upgrade(self.__level,self.__stats)
    
    @property
    def stats(self):
        return self.__stats
    
    @property
    def name(self):
        return self.__name
    
    def __eq__(self, value):
        if isinstance(value, PassiveItem):
            return value.__name == self.__name
        return False

    def can_be_upgraded(self):
        return self.__upgrade.max_level > self.__level
    
    def get_next_level_data(self):
        return self.__upgrade.get_upgrade_data(self.__level)
    
    def get_unlock_info(self):
        return self.__upgrade.unlock_info

    def serialize(self) -> dict:
        return {"name": self.__name, "level": self.__level}

    def deserialize(data : dict):
        return PassiveItem(data["name"], data["level"])
        #WeaponFactory.get_weapon_by_name(data["name"], data["level"])
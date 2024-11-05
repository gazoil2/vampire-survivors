from business.weapons.stats import ProjectileStats, ProjectileStatsMultiplier, PlayerStats
from business.weapons.exception import InvalidLevelUp
import json

class Upgrade:
    DEFAULT_UPGRADE_PATH = "data/upgrades/item_data.json"
    def __init__(self, weapon_name: str, json_file: str = "data/upgrades/item_data.json"):
        self.weapon_name = weapon_name
        self.upgrades = self.__load_upgrades(json_file)
        self.type = self.upgrades.get("type")

    def __load_upgrades(self, json_file: str) -> dict:
        """Load upgrades from a JSON file."""
        with open(json_file, 'r') as f:
            data = json.load(f)
        return data.get(self.weapon_name, {})

    def apply_upgrade(self, level: int, stats: ProjectileStats| PlayerStats) -> ProjectileStats | PlayerStats:
        """Apply the upgrade based on the weapon level."""
        if self.max_level < level:
            raise InvalidLevelUp(f"No upgrade data available for level {level} for item ")
        if self.type == "passive":
            return self.__apply_passive_upgrade(stats)
        elif self.type == "weapon":
            level -= 2
            return self.__apply_weapon_upgrade(stats, level)
        # Get the upgrade data (delta) for the specified level
        
        
        return stats

    def __apply_passive_upgrade(self, stats : PlayerStats):
        affects = self.upgrades["affects"]
        increase = self.upgrades["increase"]
        if affects == "power":
            stats.projectile_stats.power += increase
        elif affects == "velocity":
            stats.projectile_stats.velocity += increase
        elif affects == "duration":
            stats.projectile_stats.duration += increase
        elif affects == "area_of_effect":
            stats.projectile_stats.area_of_effect += increase
        elif affects == "reload_time":
            stats.projectile_stats.reload_time += increase
        elif affects == "max_health":
            stats.max_health += increase
        elif affects == "recovery":
            stats.recovery += increase
        elif affects == "armor":
            stats.armor += increase
        elif affects =="lifes":
            stats.lifes += increase
        elif affects =="movement_speed":
            stats.movement_speed += increase
        return stats

    def __apply_weapon_upgrade(self, stats : ProjectileStats, level):
        upgrade_data = self.upgrades["levels"][level]
        # Apply deltas to current stats
        stats.damage += upgrade_data.get("damage", 0)
        stats.area_of_effect += upgrade_data.get("area_of_effect", 0)
        stats.velocity += upgrade_data.get("velocity", 0)
        stats.reload_time += upgrade_data.get("reload_time", 0)  
        stats.duration += upgrade_data.get("duration", 0)
        return stats
    
    @property
    def max_level(self) -> bool:
        return self.upgrades.get("max_level",0)

    @property
    def unlock_info(self):
        return self.upgrades.get("unlock_info", "No information found")

    def get_upgrade_data(self,level):
        if self.max_level < level:
            raise InvalidLevelUp(f"No upgrade data available for level {level} for weapon {self.weapon_name}")

        if self.type == "weapon":
            level_index = level - 1
            levels = self.upgrades.get("levels", [])
            upgrade_data = levels[level_index]
            key = list(upgrade_data.keys())[0]
            value = list(upgrade_data.values())[0]
            key = key.replace("_"," ")
            if value > 0:
                return f"Increases {key} by {value}"
            else: 
                return f"Decreases {key} by {value}"
            
        
        if self.type == "passive":
            affects = self.upgrades.get("affects")
            increase = self.upgrades.get("increase")
            if increase > 0:
                return f"Increases {affects} by {increase}"
            else:
                return f"Decreases {affects} by {increase}"
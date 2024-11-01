from business.weapons.stats import ProjectileStats, ProjectileStatsMultiplier, PlayerStats
import json

class Upgrade:
    def __init__(self, weapon_name: str, json_file: str):
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
        level -= 2
        if "levels" not in self.upgrades or level >= (self.upgrades["max_level"]):
            return stats

        if self.type == "passive":
            return self.__apply_passive_upgrade(stats)
        elif self.type == "weapon":
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
        elif affects == "projectile_count":
            stats.projectile_stats.projectile_count += increase
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
        stats.damage += upgrade_data.get("d amage", 0)
        stats.area_of_effect += upgrade_data.get("area_of_effect", 0)
        stats.velocity += upgrade_data.get("velocity", 0)
        stats.reload_time += upgrade_data.get("reload_time", 0)  
        stats.duration += upgrade_data.get("duration", 0)
        stats.projectile_count += upgrade_data.get("projectile_count", 0)
        return stats
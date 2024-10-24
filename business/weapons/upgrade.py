from business.weapons.stats import ProjectileStats
import json

class Upgrade:
    def __init__(self, weapon_name: str, json_file: str):
        self.weapon_name = weapon_name
        self.upgrades = self.__load_upgrades(json_file)

    def __load_upgrades(self, json_file: str) -> dict:
        """Load upgrades from a JSON file."""
        with open(json_file, 'r') as f:
            data = json.load(f)
        return data.get(self.weapon_name, {})

    def apply_upgrade(self, level: int, stats: ProjectileStats) -> ProjectileStats:
        """Apply the upgrade based on the weapon level."""
        level -= 2
        if "levels" not in self.upgrades or level >= len(self.upgrades["levels"]):
            return stats

        # Get the upgrade data (delta) for the specified level
        upgrade_data = self.upgrades["levels"][level]

        # Apply deltas to current stats
        stats.power += upgrade_data.get("power", 0)
        stats.area_of_effect += upgrade_data.get("area_of_effect", 0)
        stats.velocity += upgrade_data.get("velocity", 0)
        stats.reload_time += upgrade_data.get("reload_time", 0)  # Adding negative value reduces reload time
        stats.duration += upgrade_data.get("duration", 0)
        stats.projectile_count += upgrade_data.get("projectile_count", 0)
        
        return stats

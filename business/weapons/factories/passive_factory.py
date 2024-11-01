import json
from typing import List
from business.weapons.stats import PlayerStats
from business.weapons.passive_item import PassiveItem
class PassiveItemFactory:
    def __init__(self, json_file: str, player_stats: PlayerStats):
        self.json_file = json_file
        self.player_stats = player_stats
    
    @staticmethod
    def load_passive_items(self) -> List[PassiveItem]:
        passive_items = []
        
        # Load the JSON data
        with open(self.json_file, 'r') as file:
            items_data = json.load(file)
        
        # Iterate through the passive items in the JSON and create PassiveItem instances
        for item_name, item_data in items_data.items():
            if item_data["type"] == "passive":
                max_level = item_data.get("max_level", 1)
                passive_item = PassiveItem(item_name, self.player_stats, self.json_file, weapon_level=max_level)
                passive_items.append(passive_item)
        
        return passive_items
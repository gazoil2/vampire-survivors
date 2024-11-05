import json
from typing import List
from business.weapons.stats import PlayerStats
from business.weapons.passive_item import PassiveItem
class PassiveItemFactory:
    
    JSON_FILE = "data/upgrades/item_data.json"
    @staticmethod
    def get_all_passive_items() -> List[PassiveItem]:
        passive_items = []
        
        # Load the JSON data
        with open(PassiveItemFactory.JSON_FILE, 'r') as file:
            items_data = json.load(file)
        
        # Iterate through the passive items in the JSON and create PassiveItem instances
        for item_name, item_data in items_data.items():
            if item_data["type"] == "passive":
                passive_item = PassiveItem(item_name)
                passive_items.append(passive_item)
        
        return passive_items

    @staticmethod
    def get_passive_by_name(name, level):
        passive = PassiveItem(name)
        for _ in range(level - 1):
            passive.upgrade()
        return passive

    @staticmethod
    def get_spinach():
        return PassiveItem("Spinach")
    
    @staticmethod
    def get_armor():
        return PassiveItem("Armor")
    
    @staticmethod
    def get_hollow_heart():
        return PassiveItem("Hollow Heart")
    
    @staticmethod
    def get_pummarola():
        return PassiveItem("Pummarola")
    
    @staticmethod
    def get_empty_tome():
        return PassiveItem("Empty Tome")
    
    @staticmethod
    def get_candelabrador():
        return PassiveItem("Candelabrador")
    
    @staticmethod
    def get_bracer():
        return PassiveItem("Bracer")
    
    @staticmethod
    def get_spellbinder():
        return PassiveItem("Spellbinder")
    
    @staticmethod
    def get_wings():
        return PassiveItem("Wings")
    
    @staticmethod
    def get_attractorb():
        return PassiveItem("Attractorb")
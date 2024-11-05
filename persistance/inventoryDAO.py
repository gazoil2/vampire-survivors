import json
from business.weapons.interfaces import IInventory
from business.weapons.inventory import Inventory
from business.weapons.factories.passive_factory import PassiveItemFactory
from business.weapons.factories.weapon_factory import WeaponFactory
class InventoryDao:
    def __init__(self, json_path):
        self.__json_path = json_path

    def load_inventory(self) -> IInventory:
        data = self.__read_from_json()
        weapons = []
        passives = []
        for weapon_dict in data.get("weapons",[]):
            weapons.append(WeaponFactory.get_weapon_by_name(weapon_dict["name"], weapon_dict["level"]))
        
        for passive_dict in data.get("passives",[]):
            passives.append(PassiveItemFactory.get_passive_by_name(passive_dict["name"], passive_dict["level"]))

        if weapons == []:
            weapons.append(WeaponFactory.get_green_wand())
        
        return Inventory(weapons,passives)
    
    def save_inventory(self, inventory : IInventory):
        data = self.__read_from_json()
        weapon_dict = {"weapons": []}
        for weapon in inventory.get_weapons():
            weapon_dict["weapons"].append(weapon.to_dict())
        
        passive_dict = {"passives": []}
        for passive in inventory.get_passives():
            passive_dict["passives"].append(passive.to_dict())
        data.update(weapon_dict)
        data.update(passive_dict)
        self.__write_to_json(data)

    def __write_to_json(self, data):
        with open(self.__json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

    def __read_from_json(self) -> dict:
        with open(self.__json_path, 'r') as json_file:
            return json.load(json_file)
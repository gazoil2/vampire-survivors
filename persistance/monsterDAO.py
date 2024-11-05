import json
from typing import List
from business.entities.interfaces import IMonster
from business.entities.monster import Monster, MonsterStats
from presentation.sprite import MonsterSprite
class MonsterDAO:
    def __init__(self, json_path):
        self.__json_path = json_path

    def save_monsters(self, monsters: List[IMonster]):
        data = self.__read_from_json()
        monster_dict = {"Monsters": []}
        for monster in monsters:
            monster_dict["Monsters"].append(monster.serialize())
        
        data.update(monster_dict)
        self.__write_to_json(data)        
    
    def load_monsters(self)-> List[IMonster]:
        data = self.__read_from_json()
        monsters = []
        for monster_dict in data.get("Monsters",[]):
            monsters.append(Monster.deserialize(monster_dict))
        return monsters

    def __write_to_json(self, data):
        with open(self.__json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

    def __read_from_json(self) -> dict:
        with open(self.__json_path, 'r') as json_file:
            return json.load(json_file)
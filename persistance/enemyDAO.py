import json
from typing import List
from business.entities.interfaces import IMonster
from business.entities.monster import Monster, MonsterStats
from presentation.sprite import MonsterSprite
class EnemyDAO:
    def __init__(self, json_path):
        self.__json_path = json_path

    def save_monsters(self, monsters: List[IMonster]):
        data = self.__read_from_json()
        monster_dict = {"Monsters": []}
        for monster in monsters:
            stats = monster.stats
            monster_dict["Monsters"].append({"health": monster.health, "pos_x": monster.pos_x,"pos_y":monster.pos_y, "speed":stats.speed,"damage":stats.damage,"cooldown":stats.attack_cooldown,"xp_drop": stats.xp_drop, "name": monster.name})
        
        data.update(monster_dict)
        self.__write_to_json(data)        
    
    def load_monsters(self)-> List[IMonster]:
        data = self.__read_from_json()
        monsters = []
        for monster_dict in data.get("Monsters",[]):
            monster_dict : dict
            name = monster_dict.get("name", "green_slime")
            pos_y = monster_dict.get("pos_y",1)
            pos_x = monster_dict.get("pos_x",1)
            speed = monster_dict.get("speed",1)
            health = monster_dict.get("health",1)
            damage = monster_dict.get("damage",1)
            cooldown = monster_dict.get("cooldown",1000)
            xp_drop = monster_dict.get("xp_drop",1)
            stats = MonsterStats(speed,health,damage,cooldown,xp_drop)
            monsters.append(Monster(pos_x,pos_y,MonsterSprite(pos_x,pos_y,name),stats,name))
        return monsters

    def __write_to_json(self, data):
        with open(self.__json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

    def __read_from_json(self) -> dict:
        with open(self.__json_path, 'r') as json_file:
            return json.load(json_file)
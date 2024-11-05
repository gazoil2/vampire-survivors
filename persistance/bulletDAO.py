
import json
from typing import List
from business.entities.interfaces import IBullet
from business.weapons.attack_shape import Bullet
from business.world.ingameclock import InGameClock
class BulletDAO:
    def __init__(self, json_path):
        self.__json_path = json_path

    def save_bullets(self, bullets : List[IBullet]):
        data = self.__read_from_json()
        bullets_dict = {"Bullets": []}
        for bullet in bullets:
            bullets_dict["Bullets"].append(bullet.serialize())
        data.update(bullets_dict)
        self.__write_to_json(data)        
    
    def load_bullets(self)-> List[IBullet]:
        data = self.__read_from_json()
        bullets = []
        for bullet_dict in data.get("Bullets",[]):
            bullets.append(Bullet.deserialize(bullet_dict))
        return bullets

    def __write_to_json(self, data):
        with open(self.__json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

    def __read_from_json(self) -> dict:
        with open(self.__json_path, 'r') as json_file:
            return json.load(json_file)
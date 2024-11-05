import json
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from business.entities.player import Player
from presentation.sprite import PlayerSprite
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from business.entities.interfaces import IPlayer
from persistance.inventoryDAO import IInventory
class PlayerDAO:
    def __init__(self, json_path):
        self.__json_path = json_path

    def save_player(self, player: "IPlayer"):
        data = self.__read_from_json()
        player_dict = {"Player":{"health": player.health, "experience": player.experience, "experience_to_next_level":player.experience_to_next_level,"pos_x":player.pos_x,"pos_y":player.pos_y}}
        data.update(player_dict)
        self.__write_to_json(data)        
    
    def load_player(self, inventory: IInventory)-> "IPlayer":
        data = self.__read_from_json()
        player_data : dict = data.get("Player",{})
        pos_x = player_data.get("pos_x",SCREEN_WIDTH//2)
        pos_y = player_data.get("pos_y",SCREEN_HEIGHT//2)
        experience = player_data.get("experience",0)
        player_experience_to_next_level = player_data.get("experience_to_next_level",30)
        return Player(pos_x,pos_y,PlayerSprite(pos_x,pos_y),inventory,experience,player_experience_to_next_level)

    def delete_all_data(self):
        self.__write_to_json({})

    def __write_to_json(self, data):
        with open(self.__json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

    def __read_from_json(self) -> dict:
        with open(self.__json_path, 'r') as json_file:
            return json.load(json_file)
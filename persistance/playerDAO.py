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
        player_data = player.serialize()  
        data["Player"] = player_data  
        self.__write_to_json(data)
    
    def load_player(self, inventory: IInventory) -> "IPlayer":
        data = self.__read_from_json()
        player_data: dict = data.get("Player", {})
        player_data["inventory"] = inventory
        player = Player.deserialize(player_data)
        return player

    def delete_all_data(self):
        self.__write_to_json({})

    def __write_to_json(self, data):
        with open(self.__json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def __read_from_json(self) -> dict:
        with open(self.__json_path, 'r') as json_file:
            return json.load(json_file)

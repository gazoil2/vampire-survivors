import json
from typing import List
from business.entities.interfaces import IExperienceGem
from business.entities.experience_gem import ExperienceGem
class xpDAO:
    def __init__(self, json_path):
        self.__json_path = json_path
    
    def save_xp(self, experience : List[IExperienceGem]):
        data = self.__read_from_json()
        experience_dict = {"Experience": []}
        for xp in experience:
            experience_dict["Experience"].append(xp.serialize())
        data.update(experience_dict)
        self.__write_to_json(data)
    
    def load_xp(self) ->  List[IExperienceGem]:
        data = self.__read_from_json()
        experience = []
        for experience_dict in data.get("Experience",[]):
            experience_dict : dict
            experience.append(ExperienceGem.deserialize(experience_dict))
        return experience

    def __write_to_json(self, data):
        with open(self.__json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

    def __read_from_json(self) -> dict:
        try:
            with open(self.__json_path, 'r') as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            print(f"The file {self.__json_path} does not exist. Creating a new file.")
            self.__write_to_json({})  
            return {} 

    def delete_all_data(self):
        self.__write_to_json({})
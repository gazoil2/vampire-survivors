
import json
from business.world.ingameclock import InGameClock
class ClockDAO:
    def __init__(self, json_path):
        self.__json_path = json_path

    def save_time(self):
        data = self.__read_from_json()
        time_dict = {"Time": InGameClock().time_elapsed}
        data.update(time_dict)
        self.__write_to_json(data)        
    
    def load_time(self)-> float:
        data = self.__read_from_json()
        time = data.get("Time", 0)
        return time
    
    def delete_all_data(self):
        self.__write_to_json({})

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
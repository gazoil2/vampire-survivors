import unittest
import pygame
from unittest.mock import patch, mock_open, MagicMock, PropertyMock
from persistance.clockDAO import ClockDAO
from persistance.xpDAO import xpDAO
from presentation.sprite import Sprite
from business.world.ingameclock import InGameClock
from business.entities.interfaces import IExperienceGem


class TestClockDAO(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch.object(InGameClock, 'time_elapsed', new_callable=PropertyMock)
    @patch.object(ClockDAO, '_ClockDAO__read_from_json')  # Mock the reading method
    def test_save_time(self, mock_read_json, mock_time_elapsed, mock_file):
        expected_value = 42
        mock_time_elapsed.return_value = expected_value
        mock_read_json.return_value = {}  
        clock_dao = ClockDAO('mock_path.json')
        clock_dao.save_time()
        self.assertEqual(clock_dao.load_time(),expected_value)


    @patch('builtins.open', new_callable=mock_open, read_data='{"Time": 42.0}')
    def test_load_time(self, mock_file):
        clock_dao = ClockDAO('mock_path.json')
        time = clock_dao.load_time()
        self.assertEqual(time, 42.0)

class TestXpDAO(unittest.TestCase):
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump') 
    @patch('json.load')  
    def test_save_xp(self, mock_load, mock_dump, mock_file):
        mock_load.return_value = {}  
        xp_dao = xpDAO('mock_path.json')
        experience_gems = [MagicMock(spec=IExperienceGem) for _ in range(2)]
        experience_gems[0].serialize.return_value = {"pos_x": 10, "pos_y": 20, "amount": 100}
        experience_gems[1].serialize.return_value = {"pos_x": 30, "pos_y": 40, "amount": 200}
        xp_dao.save_xp(experience_gems)
        expected_data = {
            "Experience": [
                {"pos_x": 10, "pos_y": 20, "amount": 100},
                {"pos_x": 30, "pos_y": 40, "amount": 200}
            ]
        }
        mock_dump.assert_called_once_with(expected_data, mock_file(), indent=4)

        

if __name__ == "__main__":
    unittest.main()

import unittest
import pygame
from unittest.mock import MagicMock, patch, mock_open
from business.entities.experience_gem import ExperienceGem
from business.world.game_world import GameWorld
from business.world.interfaces import IMonsterSpawner, ITileMap
from business.entities.interfaces import IPlayer
from persistance.xpDAO import xpDAO


class TestGameWorldIntegration(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump') 
    @patch('json.load')  
    def test_save_experience_gems(self, mock_load, mock_dump, mock_file):
        # Setup mocks
        pygame.init()
        screen = pygame.display.set_mode((640, 480))
        mock_player = MagicMock(spec=IPlayer)
        mock_spawner = MagicMock(spec=IMonsterSpawner)
        mock_tile_map = MagicMock(spec=ITileMap)
        mock_load.return_value = {}  
        mock_xp_dao = xpDAO('mock_path.json')
        game_world = GameWorld(
            spawner=mock_spawner,
            tile_map=mock_tile_map,
            player=mock_player,
            xp_dao=mock_xp_dao, 
            enemy_dao=MagicMock(), 
            inventory_dao=MagicMock(), 
            player_dao=MagicMock(),
            clock_dao=MagicMock()
        )
        experience_gem =ExperienceGem(10,20,100)
        game_world.add_experience_gem(experience_gem)

        game_world.save_data()
        expected_data = {
            "Experience": [
                {"pos_x": 10, "pos_y": 20, "amount": 100},
            ]
        }
        mock_dump.assert_called_once_with(expected_data, mock_file(), indent=4)

        
        pygame.quit()
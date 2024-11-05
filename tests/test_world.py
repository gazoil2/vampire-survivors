import unittest
import pygame
import settings
from unittest.mock import MagicMock, patch, mock_open
from business.entities.experience_gem import ExperienceGem
from business.world.game_world import GameWorld
from business.world.interfaces import IMonsterSpawner, ITileMap
from business.weapons.factories.weapon_factory import WeaponFactory
from business.entities.interfaces import IPlayer
from persistance.xpDAO import xpDAO
from persistance.enemyDAO import EnemyDAO
from presentation.sprite import MonsterSprite
from business.entities.monster import Monster,MonsterStats
from business.weapons.stats import PlayerStats
from business.handlers.colission_handler import CollisionHandler
from business.handlers.death_handler import DeathHandler
from business.world.monster_spawner import MonsterSpawner

class TestGameWorldIntegration(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump') 
    @patch('json.load')  
    def test_save_experience_gems(self, mock_load, mock_dump, mock_file):

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
    @patch.object(xpDAO,'load_xp', return_value=[])
    @patch.object(EnemyDAO, 'load_monsters', return_value=[])
    def test_bullet_kills_enemy_in_world(self,mock_load, mock_xp):
        enemy_name = "black_slime"
        pygame.init()
        screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        mock_player = MagicMock(spec=IPlayer)
        mock_player.stats = PlayerStats.get_base_player_stats()
        mock_player.pos_x = settings.SCREEN_WIDTH // 2
        mock_player.pos_y = settings.SCREEN_HEIGHT // 2
        mock_player.sprite.rect.width = 0
        mock_player.sprite.rect.height = 0
        mock_player.health = 1
        mock_spawner = MagicMock(spec=IMonsterSpawner)
        mock_tile_map = MagicMock(spec=ITileMap) 
        weapon = WeaponFactory.get_spectral_wand()
        enemy_dao = EnemyDAO('mock_path.json')
        xp_dao =xpDAO('mock_path.json')
        game_world = GameWorld(
            spawner=mock_spawner,
            tile_map=mock_tile_map,
            player=mock_player,
            xp_dao=xp_dao, 
            enemy_dao=enemy_dao, 
            inventory_dao=MagicMock(), 
            player_dao=MagicMock(),
            clock_dao=MagicMock()
        )
        enemy=Monster(settings.SCREEN_WIDTH // 2,settings.SCREEN_HEIGHT // 2,MonsterSprite(settings.SCREEN_WIDTH // 2,settings.SCREEN_HEIGHT // 2,enemy_name),MonsterStats(1,1,1,1,1),enemy_name)
        weapon._Weapon__shoot(game_world)
        game_world.add_monster(enemy)
        bullets = CollisionHandler.create_masks(game_world.bullets)
        enemies = CollisionHandler.create_masks(game_world.monsters)
        CollisionHandler.handle_bullet_monster_collisions(game_world,bullets,enemies)
        DeathHandler.check_deaths(game_world)
        self.assertEqual(1,len(game_world.bullets))
        self.assertEqual(0,len(game_world.monsters))
        self.assertEqual(1,len(game_world.experience_gems))
        pygame.quit()
    
    def test_handle_bullet_monster_collision(self):
        mock_world = MagicMock()
        mock_bullet_sprite = MagicMock()
        mock_monster_sprite = MagicMock()
        bullet_mask = MagicMock()
        monster_mask = MagicMock()
        bullet_mask.overlap.return_value = True
        mock_bullet_sprite.rect = pygame.Rect(100, 100, 32, 32)
        mock_monster_sprite.rect = pygame.Rect(150, 150, 32, 32)
        mock_bullet = MagicMock()
        mock_monster = MagicMock()
        mock_bullet.sprite = mock_bullet_sprite
        mock_monster.sprite = mock_monster_sprite
        mock_world.bullets = [mock_bullet]
        mock_world.monsters = [mock_monster]
        bullet_masks = {mock_bullet_sprite: bullet_mask}
        monster_masks = {mock_monster_sprite: monster_mask}
        CollisionHandler.handle_bullet_monster_collisions(mock_world, bullet_masks, monster_masks)
        bullet_mask.overlap.assert_called_once_with(monster_mask, (50, 50))
        mock_bullet.attack.assert_called_once_with(mock_monster)
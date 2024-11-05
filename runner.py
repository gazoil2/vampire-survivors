#!/usr/bin/env python3
"""Runs the game"""
import logging

import pygame

from business.world.game_world import GameWorld
from business.world.monster_spawner import MonsterSpawner
from business.world.tile_map import TileMap
from game import Game
from business.weapons.weapon import Weapon
from business.weapons.attack_builder import GreenBulletFactory
from business.weapons.stats import ProjectileStatsMultiplier, PlayerStats, ProjectileStats
from business.weapons.factories.weapon_factory import WeaponFactory
from business.weapons.inventory import Inventory
from presentation.display import Display
from presentation.input_handler import InputHandler
from presentation.sprite import PlayerSprite
from persistance.playerDAO import PlayerDAO
from persistance.inventoryDAO import InventoryDao
from persistance.xpDAO import xpDAO
from persistance.monsterDAO import MonsterDAO
from persistance.clockDAO import ClockDAO
from persistance.bulletDAO import BulletDAO

SAVE_FILE = "data/save_file.json"


def initialize_game_world():
    """Initializes the game world"""
    monster_spawner = MonsterSpawner()
    tile_map = TileMap()
    xp_dao = xpDAO(SAVE_FILE)
    enemy_dao = MonsterDAO(SAVE_FILE)
    inventory_dao = InventoryDao(SAVE_FILE)
    player_dao = PlayerDAO(SAVE_FILE)
    clock_dao = ClockDAO(SAVE_FILE)
    bullet_dao = BulletDAO(SAVE_FILE)
    return GameWorld(monster_spawner, tile_map, player_dao.load_player(inventory_dao.load_inventory()),xp_dao,enemy_dao,inventory_dao,player_dao, clock_dao, bullet_dao)


def main():
    """Main function to run the game"""
    # Initialize pygame
    pygame.init()

    # Logging configuration
    logging.basicConfig(
        level=logging.INFO,  # Change between INFO, WARNING or DEBUG as needed
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Initialize the game objects
    display = Display()
    world = initialize_game_world()
    display.load_world(world)
    input_handler = InputHandler(world)

    # Create a game instance and start it
    game = Game(display, world, input_handler)
    game.run()

    pygame.quit()


if __name__ == "__main__":
    main()

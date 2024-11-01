#!/usr/bin/env python3
"""Runs the game"""
import logging

import pygame

import settings
from business.entities.player import Player
from business.world.game_world import GameWorld
from business.world.monster_spawner import MonsterSpawner
from business.world.tile_map import TileMap
from game import Game
from business.weapons.weapon import Weapon
from business.weapons.attack_builder import GreenBulletFactory
from business.weapons.stats import ProjectileStatsMultiplier, PlayerStats, ProjectileStats
from business.weapons.factories.weapon_factory import WeaponFactory
from presentation.display import Display
from presentation.input_handler import InputHandler
from presentation.sprite import PlayerSprite, BulletSprite


def initialize_player():
    """Initializes the player object"""
    x, y = settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2
    return Player(x, y, PlayerSprite(x, y), PlayerStats.get_base_player_stats())


def initialize_game_world():
    """Initializes the game world"""
    monster_spawner = MonsterSpawner()
    tile_map = TileMap()
    player = initialize_player()
    weapon = WeaponFactory.get_shotgun()
    player.set_weapon(weapon)
    return GameWorld(monster_spawner, tile_map, player, 0)


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

    # Properly quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()

"""This module contains the MonsterSpawner class."""

import logging
import random

import pygame

import settings
from business.entities.monster import Monster
from business.world.interfaces import IGameWorld, IMonsterSpawner
from presentation.sprite import MonsterSprite
from business.handlers.cooldown_handler import CooldownHandler


class MonsterSpawner(IMonsterSpawner):
    """Spawns monsters in the game world."""
    FRAMES_UNTIL_MONSTER_SPAWN = 300
    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        self.__cooldown_handler = CooldownHandler(self.FRAMES_UNTIL_MONSTER_SPAWN)

    def update(self, world: IGameWorld):
        if self.__cooldown_handler.is_action_ready():
            self.__cooldown_handler.put_on_cooldown()
            self.spawn_monster(world)

    def spawn_monster(self, world: IGameWorld):
        random_side_to_spawn=random.randint(1,2)
        if random_side_to_spawn ==1:
            pos_x = world.player.pos_x + random.choice([settings.SCREEN_WIDTH // 2, - settings.SCREEN_WIDTH // 2])
            pos_y=  random.randint(0, settings.SCREEN_HEIGHT)
        else: 
            pos_x = random.randint(0, settings.SCREEN_WIDTH)
            pos_y =  world.player.pos_y + random.choice([settings.SCREEN_HEIGHT // 2, - settings.SCREEN_HEIGHT // 2])
        monster = Monster(pos_x, pos_y, MonsterSprite(pos_x, pos_y))
        world.add_monster(monster)
        self.__logger.debug("Spawning monster at (%d, %d)", pos_x, pos_y)

"""This module contains the MonsterSpawner class."""

import logging
import random

import pygame

import settings
from typing import List, Dict
from business.entities.monster import Monster
from business.entities.interfaces import IMonster
from business.world.interfaces import IGameWorld, IMonsterSpawner
from presentation.sprite import MonsterSprite
from business.world.ingameclock import InGameClock
from business.handlers.cooldown_handler import CooldownHandler
from business.weapons.stats import MonsterStats


class MonsterSpawner(IMonsterSpawner):
    """Spawns monsters in the game world."""
    ENEMY_SPAWN_CONFIG = {
    0: [
        {"name": "green_tiny_slime", "stats": MonsterStats(speed=1.5, health=10, damage=2, attack_cooldown=1000, xp_drop=2), "cooldown": 300, },
        {"name": "spinach", "stats": MonsterStats(speed=4.0, health=5, damage=1, attack_cooldown=1200,xp_drop=3), "cooldown": 800, }
    ],
    1: [
        {"name": "green_slime", "stats": MonsterStats(speed=1.2, health=15, damage=3, attack_cooldown=900,xp_drop=5), "cooldown": 400, },
        {"name": "red_slime", "stats": MonsterStats(speed=0.8, health=90, damage=4, attack_cooldown=1500,xp_drop=10), "cooldown": 1000, }
    ],
    2: [
        {"name": "Orc", "stats": MonsterStats(speed=1.4, health=30, damage=6, attack_cooldown=800, xp_drop=1), "cooldown": 350},
        {"name": "Witch", "stats": MonsterStats(speed=1.0, health=12, damage=5, attack_cooldown=700,xp_drop=1), "cooldown": 550}
    ],
    }
    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        self.__enemies_current_minute : List[Dict] = []
        self.__last_minute = -1

    def update(self, world: IGameWorld):
        current_minute = (InGameClock().time_elapsed / 1000) // 60
        if current_minute != self.__last_minute or self.__enemies_current_minute == []:
            self.__last_minute = current_minute
            self.__enemies_current_minute = []
            for enemy in self.ENEMY_SPAWN_CONFIG[current_minute]:
                cooldown = enemy.get("cooldown",300)
                name = enemy.get("name","green_tiny_slime")
                stats = enemy.get("stats", MonsterStats(1,1000,1,1,1))
                self.__enemies_current_minute.append({"cooldown_handler": CooldownHandler(cooldown),"name": name, "stats": stats})
        
        for enemy in self.__enemies_current_minute:
            enemy_spawn_cooldown = enemy.get("cooldown_handler")
            if enemy_spawn_cooldown.is_action_ready():
                name = enemy.get("name","green_tiny_slime")
                stats = enemy.get("stats", MonsterStats(1,1000,1,1,1))

                enemy_spawn_cooldown.put_on_cooldown()
                self.spawn_monster(world,name,stats)
        

    def spawn_monster(self, world: IGameWorld, name : str, stats : MonsterStats):
        random_side_to_spawn=random.randint(1,2)
        if random_side_to_spawn ==1:
            pos_x = world.player.pos_x + random.choice([settings.SCREEN_WIDTH // 2, - settings.SCREEN_WIDTH // 2])
            pos_y=  random.randint(0, settings.SCREEN_HEIGHT)
        else: 
            pos_x = random.randint(0, settings.SCREEN_WIDTH)
            pos_y =  world.player.pos_y + random.choice([settings.SCREEN_HEIGHT // 2, - settings.SCREEN_HEIGHT // 2])
        monster = Monster(pos_x, pos_y, MonsterSprite(pos_x, pos_y, name),stats)
        world.add_monster(monster)
        self.__logger.debug("Spawning monster at (%d, %d)", pos_x, pos_y)

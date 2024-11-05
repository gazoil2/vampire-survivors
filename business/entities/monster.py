"""This module contains the Monster class, which represents a monster entity in the game."""

from typing import List, Dict

from business.entities.entity import MovableEntity
from business.entities.interfaces import IDamageable, IMonster, IPlayer, ICanDealDamage
from business.handlers.cooldown_handler import CooldownHandler
from business.world.interfaces import IGameWorld
from business.weapons.stats import MonsterStats
from presentation.sprite import Sprite, MonsterSprite
from business.entities.experience_gem import ExperienceGem

class Monster(MovableEntity, IMonster):
    """A monster entity in the game."""
    MONSTER_ATTACK_COOLDOWN = 1000
    MONSTER_SPEED = 2
    def __init__(self, src_x: int, src_y: int, sprite: Sprite, monster_stats : MonsterStats, name :str):
        """
        Initializes a Monster entity.

        Args:
            src_x (int): Initial x-coordinate.
            src_y (int): Initial y-coordinate.
            sprite (Sprite): The sprite that represents the monster.

        Attributes:
            __health (int): Health points of the monster.
            __damage (int): Amount of damage the monster deals per attack.
            __attacked_enemies (dict[IDamageable, CooldownHandler]): 
                A dictionary to keep track of enemies (IDamageable) the monster has attacked 
                and their respective cooldowns (CooldownHandler) to prevent repeated attacks 
                within a short duration.
        """
        super().__init__(src_x, src_y, self.MONSTER_SPEED, sprite)
        self.__sprite = sprite
        self.__monster_stats = monster_stats
        self.__health: int = monster_stats.health
        self.__damage = monster_stats.damage
        self._speed = monster_stats.speed
        self.__attacked_enemies : Dict[IDamageable,CooldownHandler] = {}
        self.__name = name
        self._logger.debug("Created %s", self)

    @property
    def damage_amount(self):
        return self.__damage

    @property
    def name(self):
        return self.__name

    @property
    def stats(self):
        return self.__monster_stats

    def __get_direction_towards_the_player(self, world: IGameWorld):
        direction_x = world.player.pos_x - self.pos_x
        direction_y = world.player.pos_y - self.pos_y

        # Use a small threshold to prevent flickering when close to the player
        threshold = 1  # You can adjust this value based on your game's mechanics

        # Determine direction based on the distance, ensuring to avoid flickering
        if abs(direction_x) < threshold:
            direction_x = 0
        else:
            direction_x = 1 if direction_x > 0 else -1

        if abs(direction_y) < threshold:
            direction_y = 0
        else:
            direction_y = 1 if direction_y > 0 else -1

        return direction_x, direction_y

    def __movement_collides_with_entities(
        self, dx: float, dy: float, entities: List[IMonster], player : IPlayer
    ) -> bool:
        new_position = self.sprite.rect.move(dx, dy).inflate(-10, -10)
        priority = self._get_distance_to(player) - self.__monster_stats.speed 
        for entity in entities:
            entity : IMonster
            other_priority = entity._get_distance_to(player)
            if entity.sprite.rect.colliderect(new_position):
                if priority < other_priority:
                    return False
                else:
                    return True
        return False

    def update(self, world: IGameWorld):
        direction_x, direction_y = self.__get_direction_towards_the_player(world)
        if (direction_x, direction_y) == (0, 0):
            return
        if direction_x == 1:
            self.__sprite.flip(False)
        elif direction_x == -1:
            self.__sprite.flip(True)
        monsters = [m for m in world.monsters if m != self]
        dx, dy = direction_x * self.speed, direction_y * self.speed
        if not self.__movement_collides_with_entities(dx, dy, monsters, world.player):
            self.move(direction_x, direction_y)

        super().update(world)

    def __str__(self):
        return f"Monster(hp={self.health}, pos={self.pos_x, self.pos_y})"

    @property
    def health(self) -> int:
        return self.__health

    def take_damage(self, amount : int):
        self.__health = max(0, self.__health - amount)
        self.sprite.take_damage()
    
    def attack(self, damageable : IDamageable):
        if damageable not in self.__attacked_enemies:
            self.__attacked_enemies[damageable] = CooldownHandler(self.__monster_stats.attack_cooldown)
            damageable.take_damage(self.__damage)
        else:
            cooldown_handler = self.__attacked_enemies[damageable]
            if cooldown_handler.is_action_ready():
                damageable.take_damage(self.__damage)
                cooldown_handler.put_on_cooldown()
    
    def drop_loot(self, game_world):
        exp_gem = ExperienceGem(self._pos_x, self._pos_y, amount=self.__monster_stats.xp_drop)
        game_world.add_experience_gem(exp_gem)  
        self._logger.debug("Enemy died, dropping experience gem at %s", exp_gem)
    
    def serialize(self):
        return {
            "pos_x": self._pos_x,
            "pos_y": self._pos_y,
            "health": self.__health,
            "speed":self.stats.speed,
            "damage":self.stats.damage,
            "cooldown":self.stats.attack_cooldown,
            "xp_drop": self.stats.xp_drop, 
            "name": self.__name
        }

    def deserialize(data : dict):
        name = data.get("name", "green_slime")
        pos_y = data.get("pos_y",1)
        pos_x = data.get("pos_x",1)
        speed = data.get("speed",1)
        health = data.get("health",1)
        damage = data.get("damage",1)
        cooldown = data.get("cooldown",1000)
        xp_drop = data.get("xp_drop",1)
        stats = MonsterStats(speed,health,damage,cooldown,xp_drop)
        return Monster(pos_x,pos_y,MonsterSprite(pos_x,pos_y,name),stats,name)
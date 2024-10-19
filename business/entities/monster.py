"""This module contains the Monster class, which represents a monster entity in the game."""

from typing import List

from business.entities.entity import MovableEntity
from business.entities.interfaces import IDamageable, IMonster, IPlayer
from business.handlers.cooldown_handler import CooldownHandler
from business.world.interfaces import IGameWorld
from presentation.sprite import Sprite
from business.entities.experience_gem import ExperienceGem

class Monster(MovableEntity, IMonster):
    """A monster entity in the game."""
    MONSTER_ATTACK_COOLDOWN = 1000
    MONSTER_RECEIVE_DAMAGE_COOLDOWN = 20
    MONSTER_SPEED = 2
    def __init__(self, src_x: int, src_y: int, sprite: Sprite):
        super().__init__(src_x, src_y, self.MONSTER_SPEED, sprite)
        self.__health: int = 10
        self.__damage = 10
        self.__attack_range = 50
        self.__attack_cooldown = CooldownHandler(self.MONSTER_ATTACK_COOLDOWN)
        self.__receive_damage_cooldown = CooldownHandler(self.MONSTER_RECEIVE_DAMAGE_COOLDOWN)
        self._logger.debug("Created %s", self)

    def attack(self, target: IDamageable):
        """Attacks the target."""
        if not self.__attack_cooldown.is_action_ready():
            return

        if self._get_distance_to(target) < self.__attack_range:
            target.take_damage(self.damage_amount)
            self.__attack_cooldown.put_on_cooldown()

    @property
    def damage_amount(self):
        return self.__damage

    def __get_direction_towards_the_player(self, world: IGameWorld):
        direction_x = world.player.pos_x - self.pos_x
        if direction_x != 0:
            direction_x = direction_x // abs(direction_x)

        direction_y = world.player.pos_y - self.pos_y
        if direction_y != 0:
            direction_y = direction_y // abs(direction_y)

        return direction_x, direction_y

    def __movement_collides_with_entities(
        self, dx: float, dy: float, entities: List[IMonster], player : IPlayer
    ) -> bool:
        new_position = self.sprite.rect.move(dx, dy).inflate(-10, -10)
        priority = self._get_distance_to(player)
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

        monsters = [m for m in world.monsters if m != self]
        dx, dy = direction_x * self.speed, direction_y * self.speed
        if not self.__movement_collides_with_entities(dx, dy, monsters, world.player):
            self.move(direction_x, direction_y)

        self.attack(world.player)

        super().update(world)

    def __str__(self):
        return f"Monster(hp={self.health}, pos={self.pos_x, self.pos_y})"

    @property
    def health(self) -> int:
        return self.__health

    def take_damage(self, amount):
        self.__health = max(0, self.__health - amount)
        self.sprite.take_damage()
    
    def drop_loot(self, game_world):
        # Create an ExperienceGem at the enemy's position
        exp_gem = ExperienceGem(self._pos_x, self._pos_y, amount=1)
        # Add the exp_gem to your game world (make sure you have a reference to it)
        game_world.add_experience_gem(exp_gem)  # Replace with your actual method to add entities
        self._logger.debug("Enemy died, dropping experience gem at %s", exp_gem)
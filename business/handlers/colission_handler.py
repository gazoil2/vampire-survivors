"""Module for the CollisionHandler class."""

from typing import List
from settings import WORLD_WIDTH, WORLD_HEIGHT
from business.entities.interfaces import IBullet, IExperienceGem, IHasSprite, IMonster, IPlayer
from business.world.interfaces import IGameWorld


class CollisionHandler:
    """Handles collisions between entities in the game world."""

    @staticmethod
    def __collides_with(an_entity: IHasSprite, another_entity: IHasSprite):
        return an_entity.sprite.rect.colliderect(another_entity.sprite.rect)

    
    @staticmethod
    def __handle_bullets(bullets: List[IBullet], monsters: List[IMonster]):
        for bullet in bullets:
            for monster in monsters:
                if CollisionHandler.__collides_with(bullet, monster):
                    bullet.attack(monster)


    @staticmethod
    def __handle_monsters(monsters: List[IMonster], player: IPlayer):
        for monster in monsters:
            if CollisionHandler.__collides_with(monster,player):
                player.attack(monster)
                monster.attack(player)

    @staticmethod
    def __handle_gems(gems: List[IExperienceGem], player: IPlayer, world: IGameWorld):
        for gem in gems:
            if CollisionHandler.__collides_with(gem,player):
                player.pickup_gem(gem)
                world.remove_experience_gem(gem)
        
    @staticmethod
    def handle_collisions(world: IGameWorld):
        """Handles collisions between entities in the game world.

        Args:
            world (IGameWorld): The game world.
        """
        CollisionHandler.__handle_bullets(world.bullets, world.monsters)
        CollisionHandler.__handle_monsters(world.monsters, world.player)
        CollisionHandler.__handle_gems(world.experience_gems, world.player, world)
        world.player.update_position(
            max(0, min(world.player.pos_x, WORLD_WIDTH - world.player.sprite.rect.width)),
            max(0, min(world.player.pos_y, WORLD_HEIGHT - world.player.sprite.rect.height))
        )

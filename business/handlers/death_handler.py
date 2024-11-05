"""Module that contains the DeathHandler class."""

import settings
from business.entities.experience_gem import ExperienceGem
from business.exceptions import DeadPlayerException
from business.world.interfaces import IGameWorld


class DeathHandler:
    """Class that handles entity deaths."""

    @staticmethod
    def __is_entity_within_world_boundaries(entity):
        return (
            0 <= entity.pos_x <= settings.WORLD_WIDTH and 0 <= entity.pos_y <= settings.WORLD_HEIGHT
        )

    @staticmethod
    def check_deaths(world: IGameWorld):
        """Check if any entities have died and remove them from the game world.

        Args:
            world (IGameWorld): The game world to check for dead entities.
        """
        for monster in world.monsters:
            if monster.health <= 0 :
                monster.drop_loot(world)
                world.remove_monster(monster)
                
        
        for bullet in world.bullets:
            if bullet.health <= 0 or not DeathHandler.__is_entity_within_world_boundaries(bullet):
               world.remove_bullet(bullet)
        
        if world.player.health <= 0:
            raise DeadPlayerException
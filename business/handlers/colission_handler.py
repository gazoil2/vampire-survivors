import pygame
from typing import List
from settings import WORLD_WIDTH, WORLD_HEIGHT
from business.entities.interfaces import IBullet, IExperienceGem, IHasSprite, IMonster, IPlayer
from business.world.interfaces import IGameWorld


class CollisionHandler:
    """Handles collisions between entities in the game world."""

    @staticmethod
    def handle_collisions(world: IGameWorld):
        """Handles collisions between entities in the game world.

        Args:
            world (IGameWorld): The game world.
        """
        bullet_masks = CollisionHandler.create_masks(world.bullets)
        monster_masks = CollisionHandler.create_masks(world.monsters)
        gem_masks = CollisionHandler.create_masks(world.experience_gems)
        
        # Handle collisions
        CollisionHandler.handle_bullet_monster_collisions(world, bullet_masks, monster_masks)
        CollisionHandler.handle_player_monster_collisions(world, monster_masks)
        CollisionHandler.handle_player_gem_collisions(world, gem_masks)

        # Update player position within world bounds
        CollisionHandler.update_player_position(world)

    @staticmethod
    def create_masks(entities: List[IHasSprite]) -> dict:
        """Creates a dictionary of sprite masks for the given entities.

        Args:
            entities (List[IHasSprite]): List of entities with sprites.

        Returns:
            dict: A dictionary of sprite objects to masks.
        """
        return {entity.sprite: entity.sprite.mask for entity in entities}

    @staticmethod
    def handle_bullet_monster_collisions(world: IGameWorld, bullet_masks: dict, monster_masks: dict):
        """Handles bullet-monster collisions using sprite masks.

        Args:
            world (IGameWorld): The game world.
            bullet_masks (dict): Dictionary of bullets' sprite masks.
            monster_masks (dict): Dictionary of monsters' sprite masks.
        """
        for bullet_sprite, bullet_mask in bullet_masks.items():
            for monster_sprite, monster_mask in monster_masks.items():
                if bullet_mask.overlap(monster_mask, (monster_sprite.rect.x - bullet_sprite.rect.x, monster_sprite.rect.y - bullet_sprite.rect.y)):
                    bullet = next((b for b in world.bullets if b.sprite == bullet_sprite), None)
                    monster = next((m for m in world.monsters if m.sprite == monster_sprite), None)
                    if bullet and monster:
                        print("askdjfglsahdjflghasdfglhasdglhfhgljasfd")
                        bullet.attack(monster)  # Monster takes damage from the bullet

    @staticmethod
    def handle_player_monster_collisions(world: IGameWorld, monster_masks: dict):
        """Handles player-monster collisions using sprite masks.

        Args:
            world (IGameWorld): The game world.
            monster_masks (dict): Dictionary of monsters' sprite masks.
        """
        player_sprite = world.player.sprite
        for monster_sprite, monster_mask in monster_masks.items():
            if monster_mask.overlap(player_sprite.mask, (player_sprite.rect.x - monster_sprite.rect.x, player_sprite.rect.y - monster_sprite.rect.y)):
                monster = next((m for m in world.monsters if m.sprite == monster_sprite), None)
                if monster:
                    monster.attack(world.player)  # Monster attacks the player

    @staticmethod
    def handle_player_gem_collisions(world: IGameWorld, gem_masks: dict):
        """Handles player-gem collisions using sprite masks.

        Args:
            world (IGameWorld): The game world.
            gem_masks (dict): Dictionary of experience gems' sprite masks.
        """
        player_sprite = world.player.sprite
        for gem_sprite, gem_mask in gem_masks.items():
            if gem_mask.overlap(player_sprite.mask, (player_sprite.rect.x - gem_sprite.rect.x, player_sprite.rect.y - gem_sprite.rect.y)):
                gem = next((g for g in world.experience_gems if g.sprite == gem_sprite), None)
                if gem:
                    world.player.pickup_gem(gem)  # Player picks up the gem
                    world.remove_experience_gem(gem)  # Remove gem from the world

    @staticmethod
    def update_player_position(world: IGameWorld):
        """Updates the player's position to keep it within the world bounds.

        Args:
            world (IGameWorld): The game world.
        """
        player_sprite = world.player.sprite
        world.player.update_position(
            max(0, min(world.player.pos_x, WORLD_WIDTH - player_sprite.rect.width)),
            max(0, min(world.player.pos_y, WORLD_HEIGHT - player_sprite.rect.height))
        )

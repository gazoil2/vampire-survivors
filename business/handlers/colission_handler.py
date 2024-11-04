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
        # Group the bullets, monsters, and gems for collision checking
        bullet_group = pygame.sprite.Group([bullet.sprite for bullet in world.bullets])
        monster_group = pygame.sprite.Group([monster.sprite for monster in world.monsters])
        gem_group = pygame.sprite.Group([gem.sprite for gem in world.experience_gems])

        # Create masks for all sprites in each group
        bullet_masks = {bullet.sprite: bullet.sprite.mask for bullet in world.bullets}
        monster_masks = {monster.sprite: monster.sprite.mask for monster in world.monsters}
        gem_masks = {gem.sprite: gem.sprite.mask for gem in world.experience_gems}

        # Handle bullet-monster collisions using masks
        for bullet_sprite, bullet_mask in bullet_masks.items():
            for monster_sprite, monster_mask in monster_masks.items():
                # Check for overlap using masks
                if bullet_mask.overlap(monster_mask, (monster_sprite.rect.x - bullet_sprite.rect.x, monster_sprite.rect.y - bullet_sprite.rect.y)):
                    bullet = next((b for b in world.bullets if b.sprite == bullet_sprite), None)
                    monster = next((m for m in world.monsters if m.sprite == monster_sprite), None)
                    if bullet and monster:
                        bullet.attack(monster)  # Monster takes damage from the bullet

        # Handle player-monster collisions using masks
        player_sprite = world.player.sprite
        for monster_sprite, monster_mask in monster_masks.items():
            if monster_mask.overlap(player_sprite.mask, (player_sprite.rect.x - monster_sprite.rect.x, player_sprite.rect.y - monster_sprite.rect.y)):
                monster = next((m for m in world.monsters if m.sprite == monster_sprite), None)
                if monster:
                    monster.attack(world.player)  # Monster attacks the player

        # Handle player-gem collisions using masks
        for gem_sprite, gem_mask in gem_masks.items():
            if gem_mask.overlap(player_sprite.mask, (player_sprite.rect.x - gem_sprite.rect.x, player_sprite.rect.y - gem_sprite.rect.y)):
                gem = next((g for g in world.experience_gems if g.sprite == gem_sprite), None)
                if gem:
                    world.player.pickup_gem(gem)  # Player picks up the gem
                    world.remove_experience_gem(gem)  # Remove gem from the world

        # Update player's position to keep it within world bounds
        world.player.update_position(
            max(0, min(world.player.pos_x, WORLD_WIDTH - player_sprite.rect.width)),
            max(0, min(world.player.pos_y, WORLD_HEIGHT - player_sprite.rect.height))
        )
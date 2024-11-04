"""Module for displaying the game world."""

import pygame

import settings
from business.world.game_world import GameWorld
from presentation.camera import Camera
from presentation.interfaces import IDisplay
from presentation.tileset import Tileset
import time


class Display(IDisplay):
    """Class for displaying the game world."""

    def __init__(self):
        # Set the window display mode
        self.__screen = pygame.display.set_mode(settings.SCREEN_DIMENSION)

        # Set the window title
        pygame.display.set_caption(settings.GAME_TITLE)

        # Initialize the camera
        self.camera = Camera()

        self.__ground_tileset = self.__load_ground_tileset()
        self.__world: GameWorld = None
        self.__font_large = pygame.font.SysFont(None, 48)
        self.__font_small = pygame.font.SysFont(None, 24)

    def __load_ground_tileset(self):
        return Tileset(
            "./assets/tiles/dungeon.png", settings.TILE_WIDTH, settings.TILE_HEIGHT, 15, 7
        )

    def __render_ground_tiles(self):
        # Calculate the range of tiles to render based on the camera position
        start_col = max(0, self.camera.camera_rect.left // settings.TILE_WIDTH)
        end_col = min(
            settings.WORLD_COLUMNS, (self.camera.camera_rect.right // settings.TILE_WIDTH) + 1
        )
        start_row = max(0, self.camera.camera_rect.top // settings.TILE_HEIGHT)
        end_row = min(
            settings.WORLD_ROWS, (self.camera.camera_rect.bottom // settings.TILE_HEIGHT) + 1
        )

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                # Get the tile index from the tile map
                tile_index = self.__world.tile_map.get(row, col)
                tile_image = self.__ground_tileset.get_tile(tile_index)

                # Calculate the position on the screen
                x = col * settings.TILE_WIDTH - self.camera.camera_rect.left
                y = row * settings.TILE_HEIGHT - self.camera.camera_rect.top

                self.__screen.blit(tile_image, (x, y))

    def __draw_player_health_bar(self):
        # Get the player's health
        player = self.__world.player
        
        # Define the health bar dimensions
        bar_width = settings.TILE_WIDTH
        bar_height = 5
        bar_x = player.sprite.rect.centerx - bar_width // 2 - self.camera.camera_rect.left
        bar_y = player.sprite.rect.bottom + 5 - self.camera.camera_rect.top

        # Draw the background bar (red)
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.__screen, (255, 0, 0), bg_rect)

        # Draw the health bar (green)
        health_percentage = player.health / player.stats.max_health
        health_width = int(bar_width * health_percentage)
        health_rect = pygame.Rect(bar_x, bar_y, health_width, bar_height)
        pygame.draw.rect(self.__screen, (0, 255, 0), health_rect)

    def __draw_player_and_projectile_info(self):
        # Font settings
        font_size = 24  # Define the font size
        font_color = (255, 255, 255)  # Define the font color (white)
        margin = 10  # Define the margin between lines

        # Access player stats
        player_stats = self.__world.player.stats  # Get the PlayerStats object

        # Access projectile stats
        projectile_stats = player_stats.projectile_stats  # Get the ProjectileStatsMultiplier object

        # Prepare the text for player stats
        power_text = f"Power: {projectile_stats.power}%"  # Draw power
        health_text = f"Max Health: {player_stats.max_health}"  # Draw max health
        recovery_text = f"Recovery: {player_stats.recovery}"  # Draw recovery rate
        armor_text = f"Armor: {player_stats.armor}"  # Draw armor value
        movement_speed_text = f"Movement Speed: {player_stats.movement_speed}"  # Draw movement speed
        lifes_text = f"Lifes: {player_stats.lifes}"  # Draw remaining lives

        # Prepare the text for projectile stats
        projectile_power_text = f"Projectile Power: {projectile_stats.power}%"  # Draw projectile power
        projectile_velocity_text = f"Velocity: {projectile_stats.velocity}%"  # Draw projectile velocity
        projectile_duration_text = f"Duration: {projectile_stats.duration}%"  # Draw projectile duration
        projectile_area_of_effect_text = f"Area of Effect: {projectile_stats.area_of_effect}%"  # Draw area of effect
        projectile_reload_time_text = f"Reload Time: {projectile_stats.reload_time}%"  # Draw reload time

        # Render the text surfaces
        power_surface = self.__font_small.render(power_text, True, font_color)
        health_surface = self.__font_small.render(health_text, True, font_color)
        recovery_surface = self.__font_small.render(recovery_text, True, font_color)
        armor_surface = self.__font_small.render(armor_text, True, font_color)
        movement_speed_surface = self.__font_small.render(movement_speed_text, True, font_color)
        lifes_surface = self.__font_small.render(lifes_text, True, font_color)

        projectile_power_surface = self.__font_small.render(projectile_power_text, True, font_color)
        projectile_velocity_surface = self.__font_small.render(projectile_velocity_text, True, font_color)
        projectile_duration_surface = self.__font_small.render(projectile_duration_text, True, font_color)
        projectile_area_of_effect_surface = self.__font_small.render(projectile_area_of_effect_text, True, font_color)
        projectile_reload_time_surface = self.__font_small.render(projectile_reload_time_text, True, font_color)

        # Define vertical placement using font size, margin, and line index
        placement = {
            "player": [
                power_surface,
                health_surface,
                recovery_surface,
                armor_surface,
                movement_speed_surface,
                lifes_surface,
            ],
            "projectile": [
                projectile_power_surface,
                projectile_velocity_surface,
                projectile_duration_surface,
                projectile_area_of_effect_surface,
                projectile_reload_time_surface,
            ]
        }

        # Draw player stats on the screen
        for index, surface in enumerate(placement["player"]):
            self.__screen.blit(surface, (10, font_size * index + margin * index))  # Calculate vertical position

        # Draw projectile stats on the screen
        for index, surface in enumerate(placement["projectile"]):
            self.__screen.blit(surface, (10, font_size * (len(placement["player"]) + index) + margin * (len(placement["player"]) + index)))  # Calculate vertical position


    def __draw_time(self):
        time_elapsed= self.__world.time_elapsed
        time_elapsed /= 1000
        minutes = int(time_elapsed // 60)
        seconds = int(time_elapsed % 60)
        cronometer_text = f"Time: {minutes:02}:{seconds:02}"
        cronometer_surface = self.__font_large.render(
            cronometer_text, True, (255,255,255))
        self.__screen.blit(cronometer_surface, (10, 70))



    def __draw_player(self):
        adjusted_rect = self.camera.apply(self.__world.player.sprite.rect)
        self.__screen.blit(self.__world.player.sprite.image, adjusted_rect)

        self.__draw_player_health_bar()
        
        experience_text = self.__font_large.render(
            f"XP: {self.__world.player.experience}/{self.__world.player.experience_to_next_level}",
            True,
            (255, 255, 255),
        )
        self.__screen.blit(experience_text, (10, 10))

    def load_world(self, world: GameWorld):
        self.__world = world


    def render_pause_screen(self):
        """Draws the pause screen overlay."""
        overlay = pygame.Surface(self.__screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        pause_text = self.__font_large.render("Paused", True, (255, 255, 255))
        text_rect = pause_text.get_rect(center=(self.__screen.get_width() // 2, self.__screen.get_height() // 2))
        self.render_frame()
        self.__screen.blit(overlay, (0, 0))
        self.__draw_player_and_projectile_info()
        self.__screen.blit(pause_text, text_rect)

    def render_frame(self):
        # Update the camera to follow the player
        self.camera.update(self.__world.player.sprite.rect)

        # Render the ground tiles
        self.__render_ground_tiles()

        # Draw all the experience gems
        for gem in self.__world.experience_gems:
            if self.camera.camera_rect.colliderect(gem.sprite.rect):
                adjusted_rect = self.camera.apply(gem.sprite.rect)
                self.__screen.blit(gem.sprite.image, adjusted_rect)

        # Draw all monsters
        for monster in self.__world.monsters:
            if self.camera.camera_rect.colliderect(monster.sprite.rect):
                adjusted_rect = self.camera.apply(monster.sprite.rect)
                self.__screen.blit(monster.sprite.image, adjusted_rect)
                #mask_surface = monster.sprite.mask.to_surface()
                #mask_surface.fill((255, 255, 255), special_flags=pygame.BLEND_RGBA_MULT)
                #self.__screen.blit(mask_surface, adjusted_rect)

        # Draw the bullets
        for bullet in self.__world.bullets:
            if self.camera.camera_rect.colliderect(bullet.sprite.rect):
                adjusted_rect = self.camera.apply(bullet.sprite.rect)
                self.__screen.blit(bullet.sprite.image, adjusted_rect)
                #mask_surface = bullet.sprite.mask.to_surface()
                #mask_surface.fill((255, 255, 255), special_flags=pygame.BLEND_RGBA_MULT)
                #self.__screen.blit(mask_surface, adjusted_rect)

        # Draw the player
        self.__draw_player()
        self.__draw_time()
        
    def update_display(self):
        pygame.display.flip()
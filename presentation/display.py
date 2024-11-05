"""Module for displaying the game world."""

import pygame

import settings
import random
from business.world.game_world import GameWorld
from business.upgrades.upgradestrategy import ActionStrategy
from presentation.camera import Camera
from presentation.interfaces import IDisplay
from presentation.tileset import Tileset
from presentation.button import UpgradeButton, FramedImage, MenuButton
from business.weapons.interfaces import IInventory
from business.exceptions import ExitPauseMenu

class Display(IDisplay):
    """Class for displaying the game world."""

    def __init__(self):
        self.__screen = pygame.display.set_mode(settings.SCREEN_DIMENSION)
        pygame.display.set_caption(settings.GAME_TITLE)
        self.camera = Camera()
        self.__ground_tileset = self.__load_ground_tileset()
        self.__world: GameWorld = None
        self.__font_large = pygame.font.SysFont(None, 48)
        self.__font_small = pygame.font.SysFont(None, 24)
        self.__inventory = None
        self.__is_in_menu = False
        self.__buttons = None
        self.__pause_buttons = None

    @property
    def is_in_menu(self):
        return self.__is_in_menu
    def __load_ground_tileset(self):
        return Tileset(
            "./assets/tiles/dungeon.png", settings.TILE_WIDTH, settings.TILE_HEIGHT, 15, 7
        )

    def __render_ground_tiles(self):
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
        font_size = 24
        font_color = (255, 255, 255)  
        margin = 10  
        player_stats = self.__world.player.stats  
        projectile_stats = player_stats.projectile_stats  
        power_text = f"Power: {projectile_stats.power}%" 
        health_text = f"Max Health: {player_stats.max_health}"  
        recovery_text = f"Recovery: {player_stats.recovery}"  
        armor_text = f"Armor: {player_stats.armor}" 
        movement_speed_text = f"Movement Speed: {player_stats.movement_speed}" 
        lifes_text = f"Lifes: {player_stats.lifes}"  #

        projectile_power_text = f"Projectile Power: {projectile_stats.power}%" 
        projectile_velocity_text = f"Velocity: {projectile_stats.velocity}%"  
        projectile_duration_text = f"Duration: {projectile_stats.duration}%"  
        projectile_area_of_effect_text = f"Area of Effect: {projectile_stats.area_of_effect}%"  
        projectile_reload_time_text = f"Reload Time: {projectile_stats.reload_time}%"  

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

        for index, surface in enumerate(placement["player"]):
            self.__screen.blit(surface, (10, font_size * index + margin * index))  # Calculate vertical position

        for index, surface in enumerate(placement["projectile"]):
            self.__screen.blit(surface, (10, font_size * (len(placement["player"]) + index) + margin * (len(placement["player"]) + index)))  # Calculate vertical position


    def __draw_time(self):
        time_elapsed = self.__world.time_elapsed
        time_elapsed /= 1000
        minutes = int(time_elapsed // 60)
        seconds = int(time_elapsed % 60)
        cronometer_text = f"{minutes:02}:{seconds:02}"
        cronometer_surface = self.__font_large.render(cronometer_text, True, (255, 255, 255))
        screen_width = settings.SCREEN_WIDTH
        time_position_x = (screen_width - cronometer_surface.get_width()) // 2
        self.__screen.blit(cronometer_surface, (time_position_x, 10))



    def __draw_player(self):
        adjusted_rect = self.camera.apply(self.__world.player.sprite.rect)
        self.__screen.blit(self.__world.player.sprite.image, adjusted_rect)
        self.__draw_player_health_bar()
        self.__draw_experience_bar()

    def __draw_experience_bar(self):
        bar_width = settings.SCREEN_WIDTH
        bar_height = 20
        x_position = 0  
        y_position = settings.SCREEN_HEIGHT - bar_height  
        experience = self.__world.player.experience
        experience_to_next_level = self.__world.player.experience_to_next_level
        fill_percentage = experience / experience_to_next_level
        fill_width = int(bar_width * fill_percentage)
        pygame.draw.rect(self.__screen, (50, 50, 50), (x_position, y_position, bar_width, bar_height))
        pygame.draw.rect(self.__screen, (0, 255, 0), (x_position, y_position, fill_width, bar_height))

    def load_world(self, world: GameWorld):
        self.__world = world


    def render_pause_screen(self):
        """Draws the pause screen overlay."""
        self.__is_in_menu = True
        overlay = pygame.Surface(self.__screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with alpha for transparency
       

        # Render the "Paused" text in the center
        pause_text = self.__font_large.render("Paused", True, (255, 255, 255))
        text_rect = pause_text.get_rect(center=(self.__screen.get_width() // 2, self.__screen.get_height() // 2 - 100))
        self.__screen.blit(pause_text, text_rect)

        # Draw any additional elements like frame and player/projectile info
        self.render_frame()
        self.__screen.blit(overlay, (0, 0))
        self.__draw_player_and_projectile_info()

        # Initialize buttons if not already done (you can move this to __init__ if preferred)
        if not self.__pause_buttons:
            self.__pause_buttons = []
            height = 50
            width = 200
            self.__pause_buttons.append(MenuButton(x=settings.SCREEN_WIDTH // 2 - width // 2, y=settings.SCREEN_HEIGHT // 2 - height // 2 + height, width=width, height=height, action=[self.__world.save_data,exit], label="Save & Quit"))
            self.__pause_buttons.append(MenuButton(x=settings.SCREEN_WIDTH // 2 - width // 2, y=settings.SCREEN_HEIGHT // 2 - height , width=width, height=height, action=[self.__world.delete_data, exit], label="Delete & Quit"))
        for button in self.__pause_buttons:
            button.draw(self.__screen)
            button.update(pygame.mouse.get_pos())
            ended = button.handle_event()
            if ended:
                self.__is_in_menu = False
                self.__pause_buttons = None

    def render_upgrade_screen(self):
        overlay = pygame.Surface(self.__screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.render_frame()
        self.__screen.blit(overlay, (0, 0))
        self.__is_in_menu = True

        # Only create new buttons if they haven't been created yet (i.e., first time rendering)
        if self.__buttons is None:
            inventory = self.__world.player.inventory
            possible_actions = inventory.get_possible_actions()

            # Ensure there are at least 3 actions to choose from
            if len(possible_actions) < 3:
                choices = possible_actions  # Use all if less than 3
            else:
                choices = random.sample(possible_actions, 3)  # Randomly select 3

            button_height = 100
            button_width = 550
            button_margin = 10
            start_y = (self.__screen.get_height() - (button_height * len(choices) + button_margin * (len(choices) - 1))) // 2

            self.__buttons = []
            for index, action in enumerate(choices):
                button = UpgradeButton(
                    x=(self.__screen.get_width() - button_width) // 2,
                    y=start_y + index * (button_height + button_margin),
                    width=button_width,
                    height=button_height,
                    action_strategy=action
                )
                self.__buttons.append(button)

        # Draw the buttons
        for button in self.__buttons:
            button.draw(self.__screen)
            button.update(pygame.mouse.get_pos())
            ended = button.handle_event()
            if ended:
                self.__is_in_menu = False
                self.__buttons = None

    def __render_inventory_items(self):
        # Get weapons and passives from the inventory
        inventory = self.__world.player.inventory
        weapons = inventory.get_weapons()
        passives = inventory.get_passives()
        max_size = inventory.get_max_size()
    
        # Set initial grid parameters
        padding = 0
        x_offset, y_offset = 0, 32  # Initial position to start drawing items
        item_size = (64, 64)

        # Render weapons (first row)
        for i in range(max_size):
            x_position = x_offset + (i % 5) * (item_size[0] + padding)  # Arrange 5 items per row
            y_position = y_offset  # Weapons in the first row (same y_offset)
            try:
                weapon = weapons[i]
                self.__render_item(weapon.name, (x_position, y_position))
            except IndexError:
                self.__render_item("weapon",(x_position, y_position))

                


        # Update y_offset to place passives in the second row
        y_offset += item_size[1] + padding

        for i in range(max_size):
            x_position = x_offset + (i % 5) * (item_size[0] + padding)  # Arrange 5 items per row
            y_position = y_offset  # Weapons in the first row (same y_offset)
            if len(passives) > i:
                passive = passives[i]
                self.__render_item(passive.name, (x_position, y_position))
            else:
                self.__render_item("passive",(x_position, y_position))


    
    def __render_item(self, item_name, position: tuple):
        image_path = f"./assets/items/{item_name}.png"
        framed_image = FramedImage(image_path)
        framed_image.draw(self.__screen, position)

        
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

        # Draw the bullets
        for bullet in self.__world.bullets:
            if self.camera.camera_rect.colliderect(bullet.sprite.rect):
                adjusted_rect = self.camera.apply(bullet.sprite.rect)
                self.__screen.blit(bullet.sprite.image, adjusted_rect)
        
        for gem in self.__world.experience_gems:
            gem.sprite.update()

        # Draw the player
        self.__render_inventory_items()
        self.__draw_player()
        self.__draw_time()
        
    def update_display(self):
        pygame.display.flip()
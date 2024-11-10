"""Module for displaying the game world."""

import pygame
import sys
import settings
import random
from business.world.game_world import GameWorld
from business.upgrades.upgradestrategy import ActionStrategy
from presentation.camera import Camera
from presentation.interfaces import IDisplay
from presentation.tileset import Tileset
from presentation.button import UpgradeButton, FramedImage, MenuButton
from business.weapons.interfaces import IInventory
from business.exceptions import PausePressed, GameStart

class Display(IDisplay):
    """Class for displaying the game world."""

    def __init__(self):
        self.__screen = pygame.display.set_mode(settings.SCREEN_DIMENSION)
        pygame.display.set_caption(settings.GAME_TITLE)
        self.camera = Camera()
        self.__ground_tileset = self.__load_ground_tileset()
        self.__world: GameWorld = None
        self.__font_large = pygame.font.Font(None, 48)
        self.__font_small = pygame.font.Font(None, 24)
        self.__victorian_font_large = pygame.font.Font("./assets/typography/victorian.otf", 48)
        self.__victorian_font = pygame.font.Font("./assets/typography/victorian.otf", 36)
        self.__button_victorian_font = pygame.font.Font("./assets/typography/victorian.otf", 30)
        self.__victorian_font_small = pygame.font.Font("./assets/typography/victorian.otf", 24)
        self.__is_in_menu = False
        self.__buttons = None
        self.__pause_buttons = None
        self.__frames_rendered = 0

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
        margin = 10  # Space between lines of text
        box_margin = 20  # Space between the two boxes
        background_color = (100, 100, 100)  # Semi-transparent black for background

        player_stats = self.__world.player.stats  
        projectile_stats = player_stats.projectile_stats  
        
        # Define stat labels and values separately
        stats = {
            "player": {
                "max health": player_stats.max_health,
                "recovery": player_stats.recovery,
                "armor": player_stats.armor,
                "movement speed": player_stats.movement_speed,
            },
            "projectile": {
                "projectile power": f"{projectile_stats.power}%",
                "velocity": f"{projectile_stats.velocity}%",
                "duration": f"{projectile_stats.duration}%",
                "area of effect": f"{projectile_stats.area_of_effect}%",
                "reload time": f"{projectile_stats.reload_time}%"
            }
        }

        # Create surfaces for player and projectile stats (label and value)
        player_surfaces = []
        for label, value in stats["player"].items():
            label_surface = self.__victorian_font_small.render(f"{label}:", True, font_color)  # Stat name
            if value == 0:
                value = "_"
            value_surface = self.__victorian_font_small.render(str(value), True, font_color)    # Stat value
            player_surfaces.append((label_surface, value_surface))

        projectile_surfaces = []
        for label, value in stats["projectile"].items():
            label_surface = self.__victorian_font_small.render(f"{label}:", True, font_color)  # Stat name
            value_surface = self.__victorian_font_small.render(str(value), True, font_color)    # Stat value
            projectile_surfaces.append((label_surface, value_surface))

        # Define the positions and sizes of the boxes
        box_width = 300  # Total width for the box
        player_box_height = (font_size ) * len(player_surfaces) + margin  # Add a margin at the bottom
        projectile_box_height = (font_size ) * len(projectile_surfaces) + margin
        
        # Starting position (left side alignment for labels, right for values)
        x_pos = 10
        y_pos = 20  # Start drawing from the top
        
        # Draw player stats background box
        pygame.draw.rect(self.__screen, background_color, (x_pos - 5, y_pos - 5, box_width, player_box_height), border_radius=5)

        # Draw player stats (label left, value right)
        for index, (label_surface, value_surface) in enumerate(player_surfaces):
            label_width = label_surface.get_width()  # Get label width
            value_width = value_surface.get_width()  # Get value width

            # Align the label to the left of the box
            self.__screen.blit(label_surface, (x_pos + margin, y_pos + index * (font_size )))

            # Align the value to the right of the box
            self.__screen.blit(value_surface, (x_pos + box_width - value_width - margin, y_pos + index * (font_size )))

        # Update y_pos to draw the projectile box below the player box
        y_pos += player_box_height + box_margin  # Move below the player box with a margin

        # Draw projectile stats background box
        pygame.draw.rect(self.__screen, background_color, (x_pos - 5, y_pos - 5, box_width, projectile_box_height), border_radius=5)

        # Draw projectile stats (label left, value right)
        for index, (label_surface, value_surface) in enumerate(projectile_surfaces):
            label_width = label_surface.get_width()  # Get label width
            value_width = value_surface.get_width()  # Get value width

            # Align the label to the left of the box
            self.__screen.blit(label_surface, (x_pos + margin, y_pos + index * (font_size )))

            # Align the value to the right of the box
            self.__screen.blit(value_surface, (x_pos + box_width - value_width - margin, y_pos + index * (font_size )))





    def __draw_time(self):
        time_elapsed = self.__world.time_elapsed
        time_elapsed /= 1000
        minutes = int(time_elapsed // 60)
        seconds = int(time_elapsed % 60)
        cronometer_text = f"{minutes:02}:{seconds:02}"
        cronometer_surface = self.__victorian_font_large.render(cronometer_text, True, (255, 255, 255))
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
        self.__frames_rendered +=1
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

        ## Initialize buttons if not already done (you can move this to __init__ if preferred)
        if not self.__pause_buttons:
            self.__pause_buttons = []
            height = 50
            width = 200
            self.__pause_buttons.append(MenuButton(x=settings.SCREEN_WIDTH // 2 - width // 2, y=settings.SCREEN_HEIGHT // 2 - height  * 2 , width=width, height=height, action=[self.__trigger_pause], label="Unpause", font=self.__button_victorian_font))
            self.__pause_buttons.append(MenuButton(x=settings.SCREEN_WIDTH // 2 - width // 2, y=settings.SCREEN_HEIGHT // 2 - height // 2 , width=width, height=height, action=[self.__world.save_data,lambda:sys.exit("Exiting Game and saving data")], label="Save & Quit",font=self.__button_victorian_font))
            self.__pause_buttons.append(MenuButton(x=settings.SCREEN_WIDTH // 2 - width // 2, y=settings.SCREEN_HEIGHT // 2 + height , width=width, height=height, action=[self.__world.delete_data,lambda: sys.exit("Exiting Game and deleting data")], label="Delete & Quit",font=self.__button_victorian_font))
            
            
        for button in self.__pause_buttons:
            button.draw(self.__screen)
            button.update(pygame.mouse.get_pos())
            if self.__frames_rendered >= 30:
                ended = button.handle_event()
                if  ended:
                    self.__is_in_menu = False
                    self.__pause_buttons = None

    def __trigger_pause(self):
        self.__pause_buttons = None
        self.__is_in_menu = False
        self.__frames_rendered = 0
        raise PausePressed
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
            if not possible_actions:
                self.__is_in_menu = False
                return

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
    
    def render_home_screen(self):
        self.__is_in_menu = True
        background_image = pygame.image.load('./assets/mainscreen/main.png')
        background_image = pygame.transform.scale(background_image, (self.__screen.get_width(), self.__screen.get_height()))
        self.__screen.blit(background_image, (0, 0))


        if not self.__buttons:
            button_height = 50
            button_width = 200
            self.__buttons = [
                MenuButton(x=self.__screen.get_width() // 2 - button_width // 2, y=settings.SCREEN_HEIGHT // 2 - button_height // 2, width=button_width, height=button_height, action=[self.__game_start], label="Start Game", font=self.__victorian_font),
            ]

        # Draw and handle buttons
        for button in self.__buttons:
            button.draw(self.__screen)
            button.update(pygame.mouse.get_pos())
            if button.handle_event():
                self.__is_in_menu = False
                self.__buttons = None

    def __game_start(self):
        self.__is_in_menu = False
        self.__buttons = None
        raise GameStart

    def render_game_over_screen(self):
        self.__is_in_menu = True
        overlay = pygame.Surface(self.__screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  
        self.render_frame()
        self.__screen.blit(overlay, (0, 0))

        end_text = self.__font_large.render("Game Over", True, (255, 0, 0))

        text_rect = end_text.get_rect(center=(self.__screen.get_width() // 2, self.__screen.get_height() // 3))
        self.__screen.blit(end_text, text_rect)

        if not self.__buttons:
            button_height = 50
            button_width = 200
            start_y = text_rect.bottom + 50  

            self.__buttons = [
                MenuButton(x=self.__screen.get_width() // 2 - button_width // 2, y=start_y, width=button_width, height=button_height, action=[self.__world.restart_game_world], label="Restart Game"),
                MenuButton(x=self.__screen.get_width() // 2 - button_width // 2, y=start_y + 60, width=button_width, height=button_height, action=[sys.exit], label="Quit")
            ]

        # Draw and handle buttons
        for button in self.__buttons:
            button.draw(self.__screen)
            button.update(pygame.mouse.get_pos())
            if button.handle_event():
                self.__is_in_menu = False
                self.__buttons = None

        # Render the overlay and the buttons
        

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
        framed_image = FramedImage(image_path, (64,64))
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
import pygame
from business.weapons.interfaces import IActionStrategy
from typing import Callable

import pygame

import pygame

class FramedImage:
    def __init__(self, image_path: str, size: tuple = (64,64), frame_color=(255, 215, 0), frame_thickness=4):
        self.image = pygame.image.load(image_path).convert_alpha()  # Load image with transparency
        self.image = pygame.transform.scale(self.image, size)  # Scale the image to the desired size
        self.frame_color = frame_color  # Color of the frame (gold by default)
        self.frame_thickness = frame_thickness  # Thickness of the frame

    def draw(self, surface: pygame.Surface, position: tuple):
        # Get image rect based on the position (midleft of the button)
        image_rect = self.image.get_rect(midleft=position)

        # Draw the gold frame around the image
        pygame.draw.rect(surface, self.frame_color, image_rect.inflate(self.frame_thickness, self.frame_thickness), self.frame_thickness)

        # Blit the image onto the surface
        surface.blit(self.image, image_rect)





class UpgradeButton:
    ITEM_FOLDER = "./assets/items/"
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 action_strategy: IActionStrategy):
        self.rect = pygame.Rect(x, y, width, height)
        self.action_strategy = action_strategy
        self.font = pygame.font.Font(None, 36) 
        self.hovered = False  
        image_path = self.ITEM_FOLDER + action_strategy.name + ".png"
        image_size = (height - 10, height - 10)  
        self.framed_image = FramedImage(image_path, image_size)

    def draw(self, surface: pygame.Surface):
        color = (100, 100, 100) if self.hovered else (50, 50, 50)
        pygame.draw.rect(surface, color, self.rect)

        self.framed_image.draw(surface, (self.rect.left + 10, self.rect.centery))

        header_surface = self.font.render(self.action_strategy.name, True, (255, 255, 255))
        description_surface = self.font.render(self.action_strategy.description, True, (255, 255, 255))

        text_padding = self.rect.height - 10 + 20
        header_rect = header_surface.get_rect(midleft=(self.rect.left + text_padding, self.rect.top + 20))
        description_rect = description_surface.get_rect(midleft=(self.rect.left + text_padding, self.rect.bottom - 20))

        surface.blit(header_surface, header_rect)
        surface.blit(description_surface, description_rect)

    def update(self, mouse_pos: tuple):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self):
        if self.hovered and pygame.mouse.get_pressed()[0]:
            self.action_strategy.do_action()
            return True
        return False

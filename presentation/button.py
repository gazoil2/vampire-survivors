import pygame
from business.weapons.interfaces import IActionStrategy
from typing import Callable
class Button:
    def __init__(self, x: int, y: int, width: int, height: int, 
                 action_strategy: IActionStrategy):
        self.rect = pygame.Rect(x, y, width, height)
        self.action_strategy = action_strategy
        self.font = pygame.font.Font(None, 36)  # Default font with size 36
        self.hovered = False  # Track whether the button is hovered over

    def draw(self, surface: pygame.Surface):
        # Change color based on hover state
        color = (100, 100, 100) if self.hovered else (50, 50, 50)
        pygame.draw.rect(surface, color, self.rect)

        # Render header and description from the ActionStrategy
        header_surface = self.font.render(self.action_strategy.name, True, (255, 255, 255))
        description_surface = self.font.render(self.action_strategy.description, True, (255, 255, 255))

        # Position text on the button
        header_rect = header_surface.get_rect(center=(self.rect.centerx, self.rect.top + 20))
        description_rect = description_surface.get_rect(center=(self.rect.centerx, self.rect.bottom - 20))

        surface.blit(header_surface, header_rect)
        surface.blit(description_surface, description_rect)

    def update(self, mouse_pos: tuple):
        # Update hover state based on mouse position
        self.hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self):
        if self.hovered and pygame.mouse.get_pressed()[0]:
            self.action_strategy.do_action()
            self.action_strategy.has_been_selected = True
            return True
        return False
import pygame
from business.weapons.interfaces import IActionStrategy
from typing import Callable, List

class FramedImage:
    def __init__(self, image_path: str, size: tuple = (64,64), frame_color=(255, 215, 0), frame_thickness=4):
        self.image = pygame.image.load(image_path).convert_alpha()  
        self.image = pygame.transform.scale(self.image, size) 
        self.frame_color = frame_color  
        self.frame_thickness = frame_thickness 

    def draw(self, surface: pygame.Surface, position: tuple):
        image_rect = self.image.get_rect(midleft=position)
        pygame.draw.rect(surface, self.frame_color, image_rect.inflate(self.frame_thickness, self.frame_thickness), self.frame_thickness)
        surface.blit(self.image, image_rect)



class MenuButton:
    def __init__(self, x: int, y: int, width: int, height: int, action: List[Callable], label: str = "", font: pygame.font.Font = None):
        """Initializes the MenuButton.
        
        Args:
            x (int): The x-coordinate of the button.
            y (int): The y-coordinate of the button.
            width (int): The width of the button.
            height (int): The height of the button.
            action (callable): The function to call when the button is clicked.
            label (str): The text label to display on the button.
            font (Font): The font that the button uses.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.actions = action 
        self.label = label
        if not font:
            self.font = pygame.font.SysFont(None, 36)
        else:
            self.font = font
        self.hovered = False  

    def draw(self, surface: pygame.Surface):
        """Draws the button on the given surface."""
        color = (100, 100, 100) if self.hovered else (50, 50, 50)
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        if self.label:
            text_surface = self.font.render(self.label, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

    def update(self, mouse_pos: tuple):
        """Updates the hover state based on mouse position."""
        self.hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self):
        """Handles the button click event. If clicked, triggers the action."""
        if self.hovered and pygame.mouse.get_pressed()[0]:
            for action in self.actions:
                action()
            return True
        return False

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

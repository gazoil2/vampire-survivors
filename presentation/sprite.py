"""Module for the Sprite class."""

import pygame

import settings
from presentation.tileset import Tileset


class Sprite(pygame.sprite.Sprite):
    """A class representing a sprite."""

    def __init__(self, image: pygame.Surface, rect: pygame.Rect, *groups):
        self._image: pygame.Surface = image
        self._rect: pygame.Rect = rect
        super().__init__(*groups)
        self.__is_in_damage_countdown = 0
        self.__original_image: pygame.Surface = image
        self._mask: pygame.mask.Mask = pygame.mask.from_surface(image)

    @property
    def image(self) -> pygame.Surface:
        """The image of the sprite.

        Returns:
            pygame.Surface: The image of the sprite.
        """
        return self._image

    @property
    def rect(self) -> pygame.Rect:
        """The rect of the sprite.

        Returns:
            pygame.Rect: The rect of the sprite. A rect is a rectangle that defines the position and size of the sprite.
        """
        return self._rect

    @property
    def mask(self) -> pygame.mask.Mask:
        """The mask of the sprite.

        Returns:
            pygame.mask.Mask: The mask of the sprite.
        """
        return self._mask

    def update_pos(self, pos_x: float, pos_y: float):
        """Update the position of the sprite.

        Args:
            pos_x (float): The x-coordinate of the sprite.
            pos_y (float): The y-coordinate of the sprite.
        """
        self._rect.center = (int(pos_x), int(pos_y))

    def __restore_image(self):
        self._image = self.__original_image.copy()

    def __change_color(self, color: tuple[int, int, int]):
        self._image = self._image.copy()  # Make a copy of the original image
        self._image.fill(color, special_flags=pygame.BLEND_MULT)  # Change color
        self._image.set_colorkey((0, 0, 0))  # Set transparency if necessary

    def __decrease_damage_countdown(self):
        self.__is_in_damage_countdown -= 1
        if self.__is_in_damage_countdown <= 0:
            self.__is_in_damage_countdown = 0
            self.__restore_image()

    def take_damage(self):
        """Take damage."""
        self.__change_color((255, 0, 0))
        self.__is_in_damage_countdown = 30

    def update(self, *args, **kwargs):
        """Update the sprite behavior"""
        super().__init__(*args, **kwargs)
        if self.__is_in_damage_countdown > 0:
            self.__decrease_damage_countdown()

    def scale_image(self, scale_factor: float):
        """Scales the image by a scale factor.

        Args:
            scale_factor (float): The factor by which to scale the image.
        """
        original_size = self.__original_image.get_size()
        new_width = int(original_size[0] * scale_factor)
        new_height = int(original_size[1] * scale_factor)
        
        # Scale the image
        self._image = pygame.transform.scale(self._image, (new_width, new_height))
        
        # Update the mask
        self._mask = pygame.mask.from_surface(self._image)
        
        # Update the rect size and center to maintain position
        self._rect = self._image.get_rect(center=self.rect.center)


    def rotate(self, angle: float):
        """Rotate the sprite's image by the specified angle.

        Args:
            angle (float): The angle in degrees to rotate the image.
        """
        # Rotate the image
        self._image = pygame.transform.rotate(self._image, angle)
        
        # Update the mask
        self._mask = pygame.mask.from_surface(self._image)
        
        # Update the rect to maintain the center position
        self._rect = self._image.get_rect(center=self._rect.center)

    def flip(self, horizontal: bool = False, vertical: bool = False):
        """Flip the sprite's image horizontally and/or vertically.

        Args:
            horizontal (bool): If True, flip the image horizontally.
            vertical (bool): If True, flip the image vertically.
        """
        # Flip the image based on the arguments
        self._image = pygame.transform.flip(self.__original_image, horizontal, vertical)
        
        # Update the mask
        self._mask = pygame.mask.from_surface(self._image)
        
        # Update the rect to maintain the center position
        self._rect = self._image.get_rect(center=self._rect.center)


#
#class PlayerSprite(Sprite):
#    """A class representing the player sprite."""
#
#    ASSET = "./assets/player/necromancer.png"
#    IDLE_POSITIONS = [0,1,2,3,4,5,6,7]
#    WALKING_POSITIONS = [18,19,20,21,22,23,24,25]
#    SCALE = 5
#
#    def __init__(self, pos_x: float, pos_y: float):
#        self.__tile_set = Tileset(PlayerSprite.ASSET,160,128,17,7)
#        image: pygame.Surface = self.__tile_set.get_tile(0)
#        scaled_dimensions = tuple(d * self.SCALE for d in settings.TILE_DIMENSION)
#        image = pygame.transform.scale(image, scaled_dimensions).convert_alpha()
#        rect: pygame.Rect = image.get_rect(center=(int(pos_x), int(pos_y)))
#        super().__init__(image, rect)
#
class PlayerSprite(Sprite):
    """A class representing the player sprite."""

    ASSET = "./assets/adventurer-idle-00.png"

    def __init__(self, pos_x: float, pos_y: float):
        image: pygame.Surface = pygame.image.load(PlayerSprite.ASSET).convert_alpha()
        image = pygame.transform.scale(image, settings.TILE_DIMENSION)
        rect: pygame.Rect = image.get_rect(center=(int(pos_x), int(pos_y)))

        super().__init__(image, rect)


class MonsterSprite(Sprite):
    """A class representing the monster sprite."""

    ASSET_FOLDER = "./assets/enemies/"

    def __init__(self, pos_x: float, pos_y: float, file_name : str):
        image: pygame.Surface = pygame.image.load(MonsterSprite.ASSET_FOLDER + file_name + ".png").convert_alpha()
        image = pygame.transform.scale(image, settings.TILE_DIMENSION)
        rect: pygame.rect = image.get_rect(center=(int(pos_x), int(pos_y)))
        self.__flipped = False
        super().__init__(image, rect)
    

    def flip(self, horizontal = False, _ = False):
        if horizontal != self.__flipped:
            self.__flipped = horizontal
            return super().flip(horizontal, False)




class ImageSprite(Sprite):
    def __init__(self, pos_x: float, pos_y: float, image_to_load : str):
        image : pygame.Surface  = pygame.image.load(image_to_load).convert_alpha()
        image = pygame.transform.scale(image, settings.TILE_DIMENSION)
        rect: pygame.Rect = image.get_rect(center=(int(pos_x), int(pos_y)))
        super().__init__(image, rect)

class CircleBullet(Sprite):
    """A class representing a circle bullet."""
    def __init__(self, pos_x: float, pos_y: float, radius: int = 5, color = (0,0,0)):
        # Create a surface with alpha transparency
        image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)  
        # Draw a green circle
        pygame.draw.circle(image, color, (radius, radius), radius)  
        rect: pygame.Rect = image.get_rect(center=(int(pos_x), int(pos_y)))

        super().__init__(image, rect)

class ExperienceGemSprite(Sprite):
    """A class representing the experience gem sprite."""

    ASSET = "./assets/experience_gems.png"

    def __init__(self, pos_x: float, pos_y: float):
        tileset = Tileset(
            ExperienceGemSprite.ASSET, settings.TILE_HEIGHT, settings.TILE_HEIGHT, 2, 2
        )
        image: pygame.Surface = tileset.get_tile(0)
        rect: pygame.Rect = image.get_rect(center=(int(pos_x), int(pos_y)))

        super().__init__(image, rect)

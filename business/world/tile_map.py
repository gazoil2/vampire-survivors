"""Module that contains the TileMap class."""

import settings
from business.world.interfaces import ITileMap
import random

class TileMap(ITileMap):
    """Class that represents the tile map of the game world."""

    def __init__(self):
        self.map_data = self.__generate_tile_map()

    def __generate_tile_map(self):
        tile_map = []
        special_tiles = [13]

        for y in range(settings.WORLD_ROWS):
            row = []
            for x in range(settings.WORLD_COLUMNS):
                # Assign corners
                if x == 0 and y == 0:
                    tile_index = 17  # Top-left corner
                elif x == settings.WORLD_COLUMNS - 1 and y == 0:
                    tile_index = 26  # Top-right corner
                elif x == 0 and y == settings.WORLD_ROWS - 1:
                    tile_index = 77  # Bottom-left corner
                elif x == settings.WORLD_COLUMNS - 1 and y == settings.WORLD_ROWS - 1:
                    tile_index = 86  # Bottom-right corner

                # Assign walls
                elif y == 0:
                    tile_index = 34  # Top wall
                elif y == settings.WORLD_ROWS - 1:
                    tile_index = 78  # Bottom wall
                elif x == 0:
                    tile_index = 47  # Left wall
                elif x == settings.WORLD_COLUMNS - 1:
                    tile_index = 56  # Right wall

                # Ground tiles touching walls
                elif x == 1 and y == 1:
                    tile_index = 48  # Touching top and left walls
                elif x == settings.WORLD_COLUMNS - 2 and y == 1:
                    tile_index = 55  # Touching top and right walls
                elif x == 1 and y == settings.WORLD_ROWS - 2:
                    tile_index = 63  # Touching bottom and left walls
                elif x == settings.WORLD_COLUMNS - 2 and y == settings.WORLD_ROWS - 2:
                    tile_index = 70  # Touching bottom and right walls

                # Ground tiles adjacent to just one wall
                elif x == 1 and y != 0 and y != settings.WORLD_ROWS - 1:
                    tile_index = 63  # Ground touching left wall
                elif x == settings.WORLD_COLUMNS - 2 and y != 0 and y != settings.WORLD_ROWS - 1:
                    tile_index = 70  # Ground touching right wall
                elif y == 1 and x != 0 and x != settings.WORLD_COLUMNS - 1:
                    tile_index = 49  # Ground touching top wall
                elif y == settings.WORLD_ROWS - 2 and x != 0 and x != settings.WORLD_COLUMNS - 1:
                    tile_index = 64  # Ground touching bottom wall

                # Assign ground for interior tiles
                else:
                    if random.random() < 0.1:  # 10% chance to sprinkle a special tile
                        tile_index = random.choice(special_tiles)
                    else:
                        tile_index = 66

                # Add tile index to the row
                row.append(tile_index)

            # Add the row to the tile map
            tile_map.append(row)

        return tile_map

        

    def get(self, row, col) -> int:
        # Get the tile index at a specific row and column
        return self.map_data[row][col]

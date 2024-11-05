"""Module for the ExperienceGem class."""

from business.entities.entity import Entity
from business.entities.interfaces import IExperienceGem
from presentation.sprite import ExperienceGemSprite


class ExperienceGem(Entity, IExperienceGem):
    """Represents an experience gem in the game world."""

    def __init__(self, pos_x: float, pos_y: float, amount: int):
        super().__init__(pos_x, pos_y, ExperienceGemSprite(pos_x, pos_y, self.__determine_level(amount)))
        self._logger.debug("Created %s", self)
        self.__amount = amount

    @property
    def amount(self) -> int:
        return self.__amount

    def __determine_level(self, amount: int) -> int:
        """Determine the level of the gem based on the amount of experience."""
        thresholds = [10, 20, 30, 50, 70, 100, 150, 200, 300]  # Customize thresholds
        for level, threshold in enumerate(thresholds, start=1):
            if amount <= threshold:
                return level
        return len(thresholds)
    def __str__(self):
        return f"ExperienceGem(amount={self.amount}, pos=({self.pos_x}, {self.pos_y}))"

    def serialize(self):
        return {
            "pos_x": self._pos_x,
            "pos_y": self._pos_y,
            "amount": self.__amount
        }

    def deserialize(data : dict):
        pos_x = data.get("pos_x",0)
        pos_y = data.get("pos_y",0)
        amount = data.get("amount",1)
        return ExperienceGem(pos_x,pos_y,amount)
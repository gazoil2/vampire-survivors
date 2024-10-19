from abc import ABC,abstractmethod
from business.entities.interfaces import IAtackShape, IUpdatable
class IAtackShapeFactory:
    @abstractmethod
    def create_atack_shape(self, pos_x, pos_y) -> IAtackShape:
        """Creates an ataack"""

class IWeapon(IUpdatable):
    """Interface for all weapons"""
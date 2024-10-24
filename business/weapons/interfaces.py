from abc import ABC,abstractmethod
from business.entities.interfaces import IAtackShape, IUpdatable
from business.weapons.stats import ProjectileStats
class IAtackShapeFactory:
    @abstractmethod
    def create_atack_shape(self, pos_x, pos_y, projectile_stats : ProjectileStats) -> IAtackShape:
        """Creates an atack"""

class IWeapon(IUpdatable):
    """Interface for all weapons"""

    @abstractmethod
    def upgrade():
        """Upgrades the weapon to the next level"""
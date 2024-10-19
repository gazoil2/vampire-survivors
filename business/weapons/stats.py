from abc import ABC,abstractmethod

class IPlayerStats(ABC):
    @property
    @abstractmethod
    def power(self) -> int:
        """Gets the power of the projectile"""
    
    @power.setter
    @abstractmethod
    def power(self, value : int) :
        """Sets the power of the projectile"""
    
    @property
    @abstractmethod
    def velocity(self) -> int:
        """Gets the speed of the projectile."""
        

    @velocity.setter
    @abstractmethod
    def velocity(self, value: int):
        """Sets the speed of the projectile."""


    @property
    @abstractmethod
    def duration(self) -> int:
        """Gets the duration for which the projectile exists."""


    @duration.setter
    @abstractmethod
    def duration(self, value: int):
        """Sets the duration for which the projectile exists."""
  

    @property
    @abstractmethod
    def area_of_effect(self) -> int:
        """Gets the area of effect of the projectile."""

    @area_of_effect.setter
    @abstractmethod
    def area_of_effect(self, value: int):
        """Sets the area of effect of the projectile."""
        

    @property
    @abstractmethod
    def reload_time(self) -> int:
        """Gets the reload time for the projectile."""
        

    @reload_time.setter
    @abstractmethod
    def reload_time(self, value: int):
        """Sets the reload time for the projectile."""
        
    @property
    @abstractmethod
    def projectile_count(self) -> int:
        """Gets the number of projectiles."""
        

    @projectile_count.setter
    @abstractmethod
    def projectile_count(self, value: int):
        """Sets the number of projectiles."""
        

        
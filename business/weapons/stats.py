class ProjectileStats:
    def __init__(self, power : int, velocity: int, duration: int, area_of_effect: int, reload_time: int, projectile_count: int) -> None:
        self.__power = power
        self.__velocity = velocity
        self.__duration = duration
        self.__area_of_effect = area_of_effect
        self.__reload_time = reload_time
        self.__projectile_count = projectile_count
    @property
    def power(self) -> int:
        """Gets the power of the projectile"""
        return self.__power
    @power.setter
    def power(self, value : int) :
        """Sets the power of the projectile"""
        self.__power = value

    @property
    def velocity(self) -> int:
        """Gets the speed of the projectile."""
        return self.__velocity

    @velocity.setter
    def velocity(self, value: int):
        """Sets the speed of the projectile."""
        self.__velocity = value

    @property
    def duration(self) -> int:
        """Gets the duration for which the projectile exists."""
        return self.__duration

    @duration.setter
    def duration(self, value: int):
        """Sets the duration for which the projectile exists."""
        self.__duration = value

    @property
    def area_of_effect(self) -> int:
        """Gets the area of effect of the projectile."""
        return self.__area_of_effect

    @area_of_effect.setter
    def area_of_effect(self, value: int):
        """Sets the area of effect of the projectile."""
        self.__area_of_effect=value

    @property
    def reload_time(self) -> int:
        """Gets the reload time for the projectile."""
        return self.__reload_time

    @reload_time.setter
    def reload_time(self, value: int):
        """Sets the reload time for the projectile."""
        self.__reload_time = value

    @property
    def projectile_count(self) -> int:
        """Gets the number of projectiles."""
        return self.__projectile_count

    @projectile_count.setter
    def projectile_count(self, value: int):
        """Sets the number of projectiles."""
        self.__projectile_count = value
    
    
    def __add__(self, value : "ProjectileStats"):
        if not isinstance(value,ProjectileStats):
            raise ValueError("No se puede sumar stats con otro objeto que no es de tipo stats")
        return ProjectileStats(value.power + self.power, value.velocity + self.velocity, value.duration + self.duration , value.area_of_effect + self.area_of_effect, value.reload_time + self.reload_time, value.projectile_count + self.projectile_count)
    
    def __sub__(self, value : "ProjectileStats"):
        if not isinstance(value,ProjectileStats):
            raise ValueError("No se puede restar stats con otro objeto que no es de tipo stats")
        return ProjectileStats(value.power - self.power, value.velocity - self.velocity, value.duration - self.duration , value.area_of_effect - self.area_of_effect, value.reload_time - self.reload_time, value.projectile_count - self.projectile_count)


class PlayerStats:
    def __init__(self, max_health:int, recovery:int, armor:int, movement_speed:int, lifes:int,projectile_stats :ProjectileStats):
        self.__max_health = max_health
        self.__recovery = recovery
        self.__armor = armor
        self.__lifes = lifes
        self.__movement_speed=movement_speed
        self.__projectile_stats = projectile_stats
    
    def __add__(self, value):
        if isinstance(value,ProjectileStats):
            return PlayerStats(self.__max_health,self.__recovery,self.__armor,self.__movement_speed,self.__lifes,self.__projectile_stats + value)
        elif isinstance(value, PlayerStats):
            return PlayerStats(value.max_health + self.__max_health,self.__recovery,self.__armor,self.__movement_speed,self.__lifes,self.__projectile_stats + value)
    
    def __sub__(self, value : "ProjectileStats"):
        if not isinstance(value,ProjectileStats):
            raise ValueError("No se puede restar stats con otro objeto que no es de tipo stats")
        return ProjectileStats(value.power - self.power, value.velocity - self.velocity, value.duration - self.duration , value.area_of_effect - self.area_of_effect, value.reload_time - self.reload_time, value.projectile_count - self.projectile_count)
    
    @property
    def max_health(self):
        return self.__max_health
class ProjectileStats:
    @staticmethod
    def get_empty_projectile_stats():
        return ProjectileStats(0,0,0,0,0,0)
    @staticmethod
    def get_base_projectile_stats():
        return ProjectileStats(100,100,100,100,300,1)
    def __init__(self, power : int, velocity: int, duration: int, area_of_effect: int, reload_time: int, projectile_count: int) -> None:
        self.__power = power
        self.__velocity = velocity
        self.__duration = duration
        self.__area_of_effect = area_of_effect
        self.__reload_time = reload_time
        self.__projectile_count = projectile_count

    @property
    def power(self) -> int:
        """Gets the power of the projectile (percentage)."""
        return self.__power
    
    @power.setter
    def power(self, value: int) -> None:
        """Sets the power of the projectile (percentage)."""
        self.__power = value
    
    @property
    def velocity(self) -> int:
        """Gets the velocity of the projectile (percentage)."""
        return self.__velocity
    
    @velocity.setter
    def velocity(self, value: int) -> None:
        """Sets the velocity of the projectile (percentage)."""
        self.__velocity = value
    
    @property
    def duration(self) -> int:
        """Gets the duration the projectile exists (percentage)."""
        return self.__duration
    
    @duration.setter
    def duration(self, value: int) -> None:
        """Sets the duration the projectile exists (percentage)."""
        self.__duration = value
    
    @property
    def area_of_effect(self) -> int:
        """Gets the area of effect of the projectile (percentage)."""
        return self.__area_of_effect
    
    @area_of_effect.setter
    def area_of_effect(self, value: int) -> None:
        """Sets the area of effect of the projectile (percentage)."""
        self.__area_of_effect = value
    
    @property
    def reload_time(self) -> int:
        """Gets the reload time of the projectile (in milliseconds)."""
        return self.__reload_time
    
    @reload_time.setter
    def reload_time(self, value: int) -> None:
        """Sets the reload time of the projectile (in milliseconds)."""
        self.__reload_time = value
    
    @property
    def projectile_count(self) -> int:
        """Gets the number of projectiles (integer)."""
        return self.__projectile_count
    
    @projectile_count.setter
    def projectile_count(self, value: int) -> None:
        """Sets the number of projectiles (integer)."""
        self.__projectile_count = value
    
    def __add__(self, value: "ProjectileStats") -> "ProjectileStats":
        """Adds two ProjectileStats objects."""
        if not isinstance(value, ProjectileStats):
            raise ValueError("Cannot add stats with an object that is not of type ProjectileStats")
        return ProjectileStats(
            value.power + self.power, 
            value.velocity + self.velocity, 
            value.duration + self.duration, 
            value.area_of_effect + self.area_of_effect, 
            value.reload_time + self.reload_time, 
            value.projectile_count + self.projectile_count
        )
    
    def __sub__(self, value: "ProjectileStats") -> "ProjectileStats":
        """Subtracts one ProjectileStats object from another."""
        if not isinstance(value, ProjectileStats):
            raise ValueError("Cannot subtract stats with an object that is not of type ProjectileStats")
        return ProjectileStats(
            self.power - value.power, 
            self.velocity - value.velocity, 
            self.duration - value.duration, 
            self.area_of_effect - value.area_of_effect, 
            self.reload_time - value.reload_time, 
            self.projectile_count - value.projectile_count
        )
    def __str__(self) -> str:
        """Return a string representation of the projectile stats."""
        return (f"ProjectileStats(power={self.__power}%, velocity={self.__velocity}%, duration={self.__duration}%, "
                f"area_of_effect={self.__area_of_effect}%, reload_time={self.__reload_time}ms, "
                f"projectile_count={self.__projectile_count})")

class PlayerStats:
    def __init__(self, max_health: int, recovery: int, armor: int, movement_speed: int, lifes: int, projectile_stats: ProjectileStats):
        self.__max_health = max_health
        self.__recovery = recovery
        self.__armor = armor
        self.__lifes = lifes
        self.__movement_speed = movement_speed
        self.__projectile_stats = projectile_stats

    @staticmethod
    def get_empty_player_stats():
        return PlayerStats(0,0,0,0,0,ProjectileStats.get_empty_projectile_stats())
    @staticmethod
    def get_base_player_stats():
        return PlayerStats(100,0,0,5,0,ProjectileStats.get_base_projectile_stats())
    @property
    def max_health(self) -> int:
        """Gets the player's max health."""
        return self.__max_health

    @max_health.setter
    def max_health(self, value: int) -> None:
        """Sets the player's max health."""
        self.__max_health = value

    @property
    def recovery(self) -> int:
        """Gets the player's health recovery rate."""
        return self.__recovery

    @recovery.setter
    def recovery(self, value: int) -> None:
        """Sets the player's health recovery rate."""
        self.__recovery = value

    @property
    def armor(self) -> int:
        """Gets the player's armor value."""
        return self.__armor

    @armor.setter
    def armor(self, value: int) -> None:
        """Sets the player's armor value."""
        self.__armor = value

    @property
    def movement_speed(self) -> int:
        """Gets the player's movement speed."""
        return self.__movement_speed

    @movement_speed.setter
    def movement_speed(self, value: int) -> None:
        """Sets the player's movement speed."""
        self.__movement_speed = value

    @property
    def lifes(self) -> int:
        """Gets the player's remaining lives."""
        return self.__lifes

    @lifes.setter
    def lifes(self, value: int) -> None:
        """Sets the player's remaining lives."""
        self.__lifes = value

    @property
    def projectile_stats(self) -> ProjectileStats:
        """Gets the player's projectile stats."""
        return self.__projectile_stats

    @projectile_stats.setter
    def projectile_stats(self, value: ProjectileStats) -> None:
        """Sets the player's projectile stats."""
        self.__projectile_stats = value

    def __add__(self, value):
        """Adds PlayerStats or ProjectileStats."""
        if isinstance(value, ProjectileStats):
            # Adds only the projectile stats
            return PlayerStats(
                self.__max_health,
                self.__recovery,
                self.__armor,
                self.__movement_speed,
                self.__lifes,
                self.__projectile_stats + value
            )
        elif isinstance(value, PlayerStats):
            # Adds both player and projectile stats
            return PlayerStats(
                self.__max_health + value.max_health,
                self.__recovery + value.recovery,
                self.__armor + value.armor,
                self.__movement_speed + value.movement_speed,
                self.__lifes + value.lifes,
                self.__projectile_stats + value.projectile_stats
            )
        else:
            raise ValueError("Cannot add PlayerStats with a non-PlayerStats or non-ProjectileStats object")

    def __sub__(self, value):
        """Subtracts PlayerStats or ProjectileStats."""
        if isinstance(value, ProjectileStats):
            # Subtract only the projectile stats
            return PlayerStats(
                self.__max_health,
                self.__recovery,
                self.__armor,
                self.__movement_speed,
                self.__lifes,
                self.__projectile_stats - value
            )
        elif isinstance(value, PlayerStats):
            # Subtract both player and projectile stats
            return PlayerStats(
                self.__max_health - value.max_health,
                self.__recovery - value.recovery,
                self.__armor - value.armor,
                self.__movement_speed - value.movement_speed,
                self.__lifes - value.lifes,
                self.__projectile_stats - value.projectile_stats
            )
        else:
            raise ValueError("Cannot subtract PlayerStats with a non-PlayerStats or non-ProjectileStats object")

    def __str__(self) -> str:
        """Return a string representation of the player stats."""
        return (f"PlayerStats(max_health={self.__max_health}, recovery={self.__recovery}, armor={self.__armor}, "
                f"movement_speed={self.__movement_speed}, lifes={self.__lifes}, "
                f"projectile_stats={str(self.__projectile_stats)})")

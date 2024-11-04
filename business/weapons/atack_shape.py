import math
from typing import List, Dict
from random import uniform
from business.entities.interfaces import IBullet, IMonster
from business.entities.entity import MovableEntity
from business.world.interfaces import IGameWorld
from business.weapons.stats import ProjectileStats
from business.handlers.cooldown_handler import CooldownHandler
from business.entities.interfaces import IDamageable
from presentation.sprite import Sprite

class NormalBullet(MovableEntity,IBullet):
    """Atack that chooses the nearest enemy"""
    def __init__(self,pos_x: float, pos_y: float,sprite : Sprite, projectile_stats: ProjectileStats):
        self.__stats = projectile_stats
        super().__init__(pos_x,pos_y,self.__stats.velocity,sprite)
        self.__sprite = sprite
        self.__direction = (0,0)
        self.__pierce = self.__stats.pierce
        self.__attacked_enemies = []
        self.__has_set_direction = False

    @property
    def damage_amount(self):
        return self.__stats.damage

    def __set_direction(self, monsters : List[IMonster]):
        if not monsters:
            raise ValueError("No hay monstruos para atacar")
        nearest_monster = min(monsters, key=lambda monster: self._get_distance_to(monster))
        self.__direction = self._get_direction_to(nearest_monster.pos_x, nearest_monster.pos_y)
        direction_x, direction_y = self.__direction
        angle = math.degrees(math.atan2(direction_y, direction_x))

        if angle < 0:
            angle += 360
        self.__sprite.scale_image(self.__stats.area_of_effect)
        self.__sprite.rotate(-angle)
        self.__has_set_direction = True
    
    def update(self, world : IGameWorld):
        if not self.__has_set_direction:
            try:
                self.__set_direction(world.monsters)
            except ValueError:
                world.remove_bullet(self)
        self.move(self.__direction[0],self.__direction[1])
        super().update(world)
    
    @property
    def health(self) -> int:
        return self.__pierce
        
    def take_damage(self, _ : int):
        pass
    
    def attack(self, damageable : IDamageable):
        if damageable not in self.__attacked_enemies:
            damageable.take_damage(self.__stats.damage)
            self.__attacked_enemies.append(damageable)
            self.__pierce -= 1

    def __str__(self) -> str:
        return f"NormalBullet at position ({self._pos_x}, {self._pos_y})"


class RandomBullet(MovableEntity, IBullet):
    """A bullet that moves in a random direction."""
    
    def __init__(self, pos_x: float, pos_y: float, sprite: Sprite, projectile_stats: ProjectileStats):
        self.__stats = projectile_stats
        super().__init__(pos_x, pos_y, self.__stats.velocity, sprite)
        self.__sprite = sprite
        self.__sprite.scale_image(self.__stats.area_of_effect)
        self.__direction = self.__get_random_direction()
        self.__pierce = self.__stats.pierce
        self.__attacked_enemies = []

    @property
    def damage_amount(self):
        return self.__stats.damage

    def __get_random_direction(self):
        """Generate a random direction as a tuple (x, y)."""
        angle = uniform(0, 360)  # Random angle in degrees
        radian_angle = math.radians(angle)
        self.__sprite.rotate(-angle)
        return (math.cos(radian_angle), math.sin(radian_angle))

    def update(self, world: IGameWorld):
        self.move(self.__direction[0], self.__direction[1])
        super().update(world)

    @property
    def health(self) -> int:
        return self.__pierce

    def take_damage(self, _ : int):
        pass

    def attack(self, damageable: IDamageable):
        if damageable not in self.__attacked_enemies:
            damageable.take_damage(self.__stats.damage)
            self.__attacked_enemies.append(damageable)
            self.__pierce -= 1

    def __str__(self) -> str:
        return f"RandomBullet at position ({self._pos_x}, {self._pos_y})"

class RotatingBullet(MovableEntity, IBullet):
    """Bullet that orbits around the player and disappears after a set duration."""
    BASE_ATTACK_RESET = 500
    BASE_ORBIT_RANGE = 60
    def __init__(self, pos_x: float, pos_y: float, sprite: Sprite, projectile_stats: ProjectileStats):
        self.__stats = projectile_stats
        sprite.scale_image(self.__stats.area_of_effect)
        sprite.rotate(90)
        super().__init__(pos_x, pos_y, projectile_stats.velocity, sprite)
        self.__angle = 0
        self.__attacked_enemies = []
        self.__reset_attack_timer = CooldownHandler(self.BASE_ATTACK_RESET)
        self.__time_out_handler = CooldownHandler(projectile_stats.duration)
 
    @property
    def health(self):
        return 1

    @property
    def damage_amount(self):
        return self.__stats.damage

    def update(self, world: IGameWorld):
        # Check if the bullet's duration has expired
        if self.__time_out_handler.is_action_ready():
            world.remove_bullet(self)  # Remove bullet from the world when its lifetime ends
            return
        if self.__reset_attack_timer.is_action_ready():
            self.__reset_attack_timer.put_on_cooldown()
            self.__attacked_enemies = []
        # Update the angle for circular motion
        self.__angle += 0.05  

        # Get player's position
        player_pos_x = world.player.pos_x
        player_pos_y = world.player.pos_y

        # Calculate the position based on orbiting around the player
        direction_x = math.cos(self.__angle) * self.BASE_ORBIT_RANGE
        direction_y = math.sin(self.__angle) * self.BASE_ORBIT_RANGE
        
        # Calculate the target position relative to the player's position
        target_pos_x = player_pos_x + direction_x
        target_pos_y = player_pos_y + direction_y

        # Use the update_position function to set the bullet's position
        self.update_position(target_pos_x, target_pos_y)

    def attack(self, damageable: IDamageable):
        """Damage a target if it hasn't already been damaged."""
        damageable.take_damage(self.__stats.damage)

    def take_damage(self, _: int):
        """Rotating bullets ignore damage since they disappear after a duration."""
        pass

    def __str__(self) -> str:
        return f"RotatingBullet at position ({self._pos_x}, {self._pos_y})"


class TrailBullet(MovableEntity, IBullet):
    """Bullet that orbits around the player and disappears after a set duration."""

    def __init__(self, pos_x: float, pos_y: float, sprite: Sprite, projectile_stats: ProjectileStats):
        self.__stats = projectile_stats
        sprite.scale_image(self.__stats.area_of_effect)

        # Use the sprite's rect to set the center position directly
        sprite.update_pos(pos_x, pos_y)

        # Call the MovableEntity constructor with the rect position
        super().__init__(sprite.rect.centerx, sprite.rect.centery, projectile_stats.velocity, sprite)
        self.__time_out_handler = CooldownHandler(projectile_stats.duration)
        self.__attacked_enemies = []

    @property
    def health(self):
        return 1

    @property
    def damage_amount(self):
        return self.__stats.damage

    def update(self, world: IGameWorld):
        # Check if the bullet's duration has expired
        if self.__time_out_handler.is_action_ready():
            world.remove_bullet(self)  # Remove bullet from the world when its lifetime ends
            return

        super().update(world)

    def attack(self, damageable: IDamageable):
        """Damage a target if it hasn't already been damaged."""
        if damageable not in self.__attacked_enemies:
            damageable.take_damage(self.__stats.damage)
            self.__attacked_enemies.append(damageable)

    def take_damage(self, _: int):
        """Rotating bullets ignore damage since they disappear after a duration."""
        pass

    def __str__(self) -> str:
        return f"RotatingBullet at position ({self._pos_x}, {self._pos_y})"

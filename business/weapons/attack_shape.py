import math
import settings
from typing import List
from random import uniform, choice
from business.entities.interfaces import IBullet, IMonster
from business.entities.entity import MovableEntity
from business.world.interfaces import IGameWorld
from business.weapons.stats import ProjectileStats
from business.handlers.cooldown_handler import CooldownHandler
from business.entities.interfaces import IDamageable
from presentation.sprite import Sprite

class Bullet(MovableEntity, IBullet):
    """Base class for all bullet types."""
    
    def __init__(self, pos_x: float, pos_y: float, sprite: Sprite, projectile_stats: ProjectileStats, bullet_type: str):
        super().__init__(pos_x, pos_y, projectile_stats.velocity, sprite)
        self._sprite = sprite
        self._stats = projectile_stats
        self._pierce = self._stats.pierce
        self._attacked_enemies = []
        self.bullet_type = bullet_type


    @property
    def damage_amount(self):
        return self._stats.damage

    @property
    def health(self) -> int:
        return self._pierce
        
    def take_damage(self, _: int):
        pass
    
    def attack(self, damageable: IDamageable):
        if damageable not in self._attacked_enemies:
            damageable.take_damage(self._stats.damage)
            self._attacked_enemies.append(damageable)
            self._pierce -= 1
    
    def serialize(self):
        return {
                'pos_x': self._pos_x,
                'pos_y': self._pos_y,
                'damage': self._stats.damage,
                'velocity': self._stats.velocity,
                'area_of_effect': self._stats.area_of_effect,
                'reload_time': self._stats.reload_time,
                'pierce': self._pierce,
                'duration': self._stats.duration,
                'bullet_type': self.bullet_type
            }
    def deserialize(data : dict):
        from business.weapons.attack_builder import BulletFactory
        pos_x = data.get("pos_x")
        pos_y = data.get("pos_y")
        damage = data.get("damage")
        velocity = data.get("velocity")
        area_of_effect = data.get("area_of_effect")
        reload_time = data.get("reload_time")
        pierce = data.get("pierce")
        duration = data.get("duration")
        type = data.get("bullet_type")
        factory = BulletFactory.get_factory_by_name(type)
        return factory.create_atack_shape(pos_x,pos_y,ProjectileStats(damage,velocity,area_of_effect,reload_time,pierce,duration))

class NormalBullet(Bullet):
    """Attack that chooses the nearest enemy."""
    TYPE = "Normalbullet"
    def __init__(self, pos_x: float, pos_y: float, sprite: Sprite, projectile_stats: ProjectileStats, type : str = None):
        if not type:
            type = self.TYPE
        super().__init__(pos_x, pos_y, sprite, projectile_stats, type)  
        self.__direction = (0, 0)
        self._sprite.scale_image(self._stats.area_of_effect)
        self.__has_set_direction = False

    def __set_direction(self, monsters: List[IMonster]):
        if not monsters:
            raise ValueError("No hay monstruos para atacar")
        nearest_monster = min(monsters, key=lambda monster: self._get_distance_to(monster))
        self.__direction = self._get_direction_to(nearest_monster.pos_x, nearest_monster.pos_y)
        direction_x, direction_y = self.__direction
        angle = math.degrees(math.atan2(direction_y, direction_x))

        if angle < 0:
            angle += 360
        
        self._sprite.rotate(-angle)
        self.__has_set_direction = True
    
    def update(self, world: IGameWorld):
        if not self.__has_set_direction:
            try:
                self.__set_direction(world.monsters)
            except ValueError:
                world.remove_bullet(self)
        self.move(self.__direction[0], self.__direction[1])
        super().update(world)

    def __str__(self) -> str:
        return f"NormalBullet at position ({self._pos_x}, {self._pos_y})"

class RandomBullet(Bullet):
    """A bullet that moves in a random direction."""
    TYPE = "RandomBullet"
    def __init__(self, pos_x: float, pos_y: float, sprite: Sprite, projectile_stats: ProjectileStats):
        super().__init__(pos_x, pos_y, sprite, projectile_stats, self.TYPE)  
        self._sprite.scale_image(self._stats.area_of_effect)
        self.__direction = self.__get_random_direction()

    def __get_random_direction(self):
        """Generate a random direction as a tuple (x, y)."""
        angle = uniform(0, 360)  # Random angle in degrees
        radian_angle = math.radians(angle)
        self._sprite.rotate(-angle)
        return (math.cos(radian_angle), math.sin(radian_angle))

    def update(self, world: IGameWorld):
        self.move(self.__direction[0], self.__direction[1])
        super().update(world)

    def __str__(self) -> str:
        return f"RandomBullet at position ({self._pos_x}, {self._pos_y})"


class RotatingBullet(Bullet):
    """Bullet that orbits around the player and disappears after a set duration."""
    TYPE = "Rotatingbullet"
    BASE_ATTACK_RESET = 500
    BASE_ORBIT_RANGE = 100

    def __init__(self, pos_x: float, pos_y: float, sprite: Sprite, projectile_stats: ProjectileStats):
        super().__init__(pos_x, pos_y, sprite, projectile_stats, self.TYPE)
        sprite.scale_image(self._stats.area_of_effect)
        sprite.rotate(90)
        self.__angle = 0
        self.__reset_attack_timer = CooldownHandler(self.BASE_ATTACK_RESET)
        self.__time_out_handler = CooldownHandler(projectile_stats.duration)

    def update(self, world: IGameWorld):
        if self.__time_out_handler.is_action_ready():
            world.remove_bullet(self)  
            return
        if self.__reset_attack_timer.is_action_ready():
            self.__reset_attack_timer.put_on_cooldown()
            self._attacked_enemies = []
        self.__angle += 0.07 * self._stats.velocity 
        player_pos_x = world.player.pos_x
        player_pos_y = world.player.pos_y
        direction_x = math.cos(self.__angle) * self.BASE_ORBIT_RANGE
        direction_y = math.sin(self.__angle) * self.BASE_ORBIT_RANGE
        target_pos_x = player_pos_x + direction_x
        target_pos_y = player_pos_y + direction_y
        self.update_position(target_pos_x, target_pos_y)

    def __str__(self) -> str:
        return f"RotatingBullet at position ({self._pos_x}, {self._pos_y})"

class SantaWaterBullet(Bullet):
    """Spawns a damage area at a random enemy position."""
    TYPE = "Trailbullet"

    def __init__(self, pos_x: float, pos_y: float, sprite: Sprite, projectile_stats: ProjectileStats):
        super().__init__(pos_x, pos_y, sprite, projectile_stats, self.TYPE)
        sprite.scale_image(self._stats.area_of_effect)
        self.__time_out_handler = CooldownHandler(self._stats.duration)
        self.__has_chose_enemy = False

    def __is_monster_on_screen(self, monster: IMonster, player, screen_width: int, screen_height: int) -> bool:
        """Check if the monster is within the screen bounds."""
        # Get the player's position as the center of the screen
        player_x, player_y = player.pos_x, player.pos_y

        # Calculate screen boundaries based on the player's position
        screen_left = player_x - (screen_width // 2)
        screen_right = player_x + (screen_width // 2)
        screen_top = player_y - (screen_height // 2)
        screen_bottom = player_y + (screen_height // 2)

        # Check if the monster's position is within the screen bounds
        return screen_left <= monster.pos_x <= screen_right and screen_top <= monster.pos_y <= screen_bottom

    def __choose_enemy(self, monsters: List[IMonster], player, screen_width: int, screen_height: int):
        """Choose a random monster on screen."""
        on_screen_monsters = [monster for monster in monsters if self.__is_monster_on_screen(monster, player, screen_width, screen_height)]
        random_monster = choice(on_screen_monsters)
        self.update_position(random_monster.pos_x, random_monster.pos_y)
        self.__has_chose_enemy = True

    def update(self, world: IGameWorld):
        if not self.__has_chose_enemy:
            try:
                if world.monsters:
                    self.__choose_enemy(world.monsters, world.player, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
                else:
                    world.remove_bullet(self)
            except ValueError:
                world.remove_bullet(self)
        
        if self.__time_out_handler.is_action_ready():
            world.remove_bullet(self) 
            return

        super().update(world)

    def __str__(self) -> str:
        return f"SantaWaterBullet at position ({self._pos_x}, {self._pos_y})"

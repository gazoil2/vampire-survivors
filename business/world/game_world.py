"""This module contains the implementation of the game world."""

from business.entities.interfaces import IBullet, IExperienceGem, IMonster, IPlayer
from business.world.interfaces import IGameWorld, IMonsterSpawner, ITileMap
from business.world.ingameclock import InGameClock
from persistance.enemyDAO import EnemyDAO
from persistance.xpDAO import xpDAO
from persistance.playerDAO import PlayerDAO
from persistance.inventoryDAO import InventoryDao
from persistance.clockDAO import ClockDAO
from persistance.bulletDAO import BulletDAO
from settings import FPS
class GameWorld(IGameWorld):
    """Represents the game world."""

    def __init__(self, spawner: IMonsterSpawner, tile_map: ITileMap, player: IPlayer, xp_dao : xpDAO, enemy_dao : EnemyDAO, inventory_dao : InventoryDao, player_dao : PlayerDAO, clock_dao : ClockDAO, bullet_dao : BulletDAO):
        self.__player: IPlayer = player
        self.__monsters: list[IMonster] = enemy_dao.load_monsters()
        self.__bullets: list[IBullet] = bullet_dao.load_bullets()
        self.__experience_gems: list[IExperienceGem] = xp_dao.load_xp()

        self.__clock = InGameClock()
        self.__clock.update(clock_dao.load_time() // 1000)
        self.tile_map: ITileMap = tile_map
        self.__xp_dao = xp_dao
        self.__enemy_dao = enemy_dao
        self.__inventory_dao = inventory_dao
        self.__player_dao = player_dao
        self.__clock_dao = clock_dao
        self.__bullet_dao = bullet_dao
        self.__monster_spawner: IMonsterSpawner = spawner

    def update(self):
        # Update the clock only when the game is running
        self.__clock.update(1 / FPS)
        self.__player.update(self)

        for monster in self.__monsters:
            monster.update(self)

        for bullet in self.__bullets:
            bullet.update(self)

        
        self.__monster_spawner.update(self)

    @property
    def time_elapsed(self):
        return self.__clock.time_elapsed

    def add_monster(self, monster: IMonster):
        self.__monsters.append(monster)

    def remove_monster(self, monster: IMonster):
        self.__monsters.remove(monster)

    def add_experience_gem(self, gem: IExperienceGem):
        self.__experience_gems.append(gem)

    def remove_experience_gem(self, gem: IExperienceGem):
        self.__experience_gems.remove(gem)

    def add_bullet(self, bullet: IBullet):
        self.__bullets.append(bullet)

    def remove_bullet(self, bullet: IBullet):
        self.__bullets.remove(bullet)

    @property
    def player(self) -> IPlayer:
        return self.__player

    @property
    def monsters(self) -> list[IMonster]:
        return self.__monsters[:]

    @property
    def bullets(self) -> list[IBullet]:
        return self.__bullets[:]

    @property
    def experience_gems(self) -> list[IExperienceGem]:
        return self.__experience_gems[:]
    
    def save_data(self):
        self.__player_dao.save_player(self.__player)
        self.__inventory_dao.save_inventory(self.__player.inventory)
        self.__clock_dao.save_time()
        self.__enemy_dao.save_monsters(self.__monsters)
        self.__xp_dao.save_xp(self.__experience_gems)
        self.__bullet_dao.save_bullets(self.__bullets)


    def delete_data(self):
        self.__player_dao.delete_all_data()
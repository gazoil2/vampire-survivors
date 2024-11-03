import unittest
from business.weapons.stats import ProjectileStatsMultiplier, ProjectileStats, PlayerStats
class TestProjectileStatsMultiplier(unittest.TestCase):

    def test_empty_projectile_stats(self):
        empty_stats = ProjectileStatsMultiplier.get_empty_projectile_stats()
        self.assertEqual(empty_stats.power, 0)

    def test_base_projectile_stats(self):
        base_stats = ProjectileStatsMultiplier.get_base_projectile_stats()
        self.assertEqual(base_stats.power, 100)

    def test_set_power(self):
        stats = ProjectileStatsMultiplier(50, 50, 50, 50, 50)
        stats.power = 75
        self.assertEqual(stats.power, 75)

    def test_set_velocity(self):
        stats = ProjectileStatsMultiplier(50, 50, 50, 50, 50)
        stats.velocity = 80
        self.assertEqual(stats.velocity, 80)

    def test_set_duration(self):
        stats = ProjectileStatsMultiplier(50, 50, 50, 50, 50)
        stats.duration = 90
        self.assertEqual(stats.duration, 90)

    def test_set_area_of_effect(self):
        stats = ProjectileStatsMultiplier(50, 50, 50, 50, 50)
        stats.area_of_effect = 60
        self.assertEqual(stats.area_of_effect, 60)

    def test_set_reload_time(self):
        stats = ProjectileStatsMultiplier(50, 50, 50, 50, 50)
        stats.reload_time = 100
        self.assertEqual(stats.reload_time, 100)

    def test_add_projectile_stats(self):
        stats1 = ProjectileStatsMultiplier(10, 20, 30, 40, 50)
        stats2 = ProjectileStatsMultiplier(5, 10, 15, 20, 25)
        result = stats1 + stats2
        self.assertEqual(result.power, 15)

    def test_sub_projectile_stats(self):
        stats1 = ProjectileStatsMultiplier(10, 20, 30, 40, 50)
        stats2 = ProjectileStatsMultiplier(5, 10, 15, 20, 25)
        result = stats1 - stats2
        self.assertEqual(result.power, 5)

class TestPlayerStats(unittest.TestCase):

    def test_empty_player_stats(self):
        empty_stats = PlayerStats.get_empty_player_stats()
        self.assertEqual(empty_stats.max_health, 0)

    def test_base_player_stats(self):
        base_stats = PlayerStats.get_base_player_stats()
        self.assertEqual(base_stats.max_health, 100)

    def test_set_max_health(self):
        stats = PlayerStats(100, 10, 20, 30, 40, ProjectileStatsMultiplier.get_empty_projectile_stats())
        stats.max_health = 150
        self.assertEqual(stats.max_health, 150)

    def test_set_recovery(self):
        stats = PlayerStats(100, 10, 20, 30, 40, ProjectileStatsMultiplier.get_empty_projectile_stats())
        stats.recovery = 15
        self.assertEqual(stats.recovery, 15)

    def test_add_player_stats(self):
        stats1 = PlayerStats(100, 10, 20, 30, 40, ProjectileStatsMultiplier(10, 20, 30, 40, 50))
        stats2 = PlayerStats(50, 5, 10, 15, 20, ProjectileStatsMultiplier(5, 10, 15, 20, 25))
        result = stats1 + stats2
        self.assertEqual(result.movement_speed, 45)

    def test_sub_player_stats(self):
        stats1 = PlayerStats(100, 10, 20, 30, 40, ProjectileStatsMultiplier(10, 20, 30, 40, 50))
        stats2 = PlayerStats(50, 5, 10, 15, 20, ProjectileStatsMultiplier(5, 10, 15, 20, 25))
        result = stats1 - stats2
        self.assertEqual(result.max_health, 50)

class TestProjectileStats(unittest.TestCase):

    def test_empty_projectile_stats(self):
        empty_stats = ProjectileStats.get_empty_stats()
        self.assertEqual(empty_stats.damage, 0)

    def test_base_projectile_stats(self):
        base_stats = ProjectileStats.get_base_stats()
        self.assertEqual(base_stats.damage, 5)

    def test_set_damage(self):
        stats = ProjectileStats(10, 20, 30, 40, 1, 500)
        stats.damage = 15
        self.assertEqual(stats.damage, 15)

    def test_multiply_projectile_stats(self):
        stats = ProjectileStats(100, 200, 50, 500, 1, 1000)
        multiplier = ProjectileStatsMultiplier(50, 50, 50, 50, 50)
        result = stats * multiplier
        self.assertEqual(result.damage, 50)

if __name__ == '__main__':
    unittest.main()

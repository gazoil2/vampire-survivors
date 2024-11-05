import unittest
from unittest.mock import MagicMock,patch
from business.weapons.attack_shape import NormalBullet, ProjectileStats
from business.entities.interfaces import IDamageable
class TestBullet(unittest.TestCase):
    def setUp(self):
        self.mock_stats = MagicMock(spec=ProjectileStats)
        self.mock_stats.velocity = 1.0  
        self.mock_stats.damage = 10  
        self.mock_stats.pierce = 3  
        self.mock_stats.area_of_effect = 1.0  
        self.bullet = NormalBullet(0, 0, MagicMock(), self.mock_stats)
    def test_bullet_movement(self):
        self.bullet.move(1, 1)  
        expected_position = (1**2 + 1**2)**0.5
        self.assertAlmostEqual(self.bullet._pos_x + self.bullet._pos_y, expected_position)
    
    def test_bullet_attack(self):
        target_mock = MagicMock(spec=[IDamageable])
        target_mock.health = 10
        target_mock.take_damage = MagicMock()
        self.bullet.attack(target_mock)
        target_mock.take_damage.assert_called_once_with(self.mock_stats.damage)

    
    

if __name__ == "__main__":
    unittest.main()

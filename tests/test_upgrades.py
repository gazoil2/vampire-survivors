import unittest
from unittest.mock import patch, mock_open
from business.weapons.stats import ProjectileStats, PlayerStats
from business.weapons.upgrade import Upgrade
from business.weapons.exception import InvalidLevelUp

class TestUpgrade(unittest.TestCase):

    def setUp(self):
        """Set up the initial stats for testing."""
        self.projectile_stats = ProjectileStats(10,10,10,10,10,10)  # damage, velocity, duration, reload_time, area_of_effect, projectile_count
        self.player_stats = PlayerStats(10,10,10,10,10,self.projectile_stats)  # max_health, recovery, projectile_stats

    @patch('builtins.open', new_callable=mock_open, read_data='{"Green Wand": {"type": "weapon", "max_level": 3, "levels": [{"damage": 5}]}}')
    def test_apply_weapon_upgrade(self, mock_file):
        """Test applying weapon upgrades to ProjectileStats."""
        upgrade = Upgrade("Green Wand")
        upgrade.apply_upgrade(1, self.projectile_stats)
        self.assertEqual(15, self.projectile_stats.damage)


    @patch('builtins.open', new_callable=mock_open, read_data='{"Bible": {"type": "passive", "max_level": 3,"affects": "max_health", "increase": 50}}')
    def test_apply_passive_upgrade(self, mock_file):
        """Test applying passive upgrades to PlayerStats."""
        upgrade = Upgrade("Bible")
        updated_stats = upgrade.apply_upgrade(2, self.player_stats)
        self.assertEqual(60, self.player_stats.max_health)

    @patch('builtins.open', new_callable=mock_open, read_data='{"Green Wand": {"type": "weapon", "max_level": 3}}')
    def test_apply_upgrade_beyond_max_level(self, mock_file):
        """Test applying an upgrade beyond the max level."""
        upgrade = Upgrade("Green Wand")
        with self.assertRaises(InvalidLevelUp):
            updated_stats = upgrade.apply_upgrade(4, self.projectile_stats)
    
    @patch('builtins.open', new_callable=mock_open, read_data='{"Green Wand": {"type": "weapon", "max_level": 3}}')
    def test_get_upgrade_data_beyond_max_level(self, mock_file):
        """Test applying an upgrade beyond the max level."""
        upgrade = Upgrade("Green Wand")
        with self.assertRaises(InvalidLevelUp):
            updated_stats = upgrade.get_upgrade_data(4)

    @patch('builtins.open', new_callable=mock_open, read_data='{"Green Wand": {"type": "weapon", "max_level": 3, "levels": [{"damage": 5}, {"area_of_effect": 0.1}, {"reload_time": -500}]}}')
    def test_get_upgrade_data(self, mock_file):
        """Test retrieving upgrade data."""
        upgrade = Upgrade("Green Wand")
        actual_data = upgrade.get_upgrade_data(1)
        expected_data = "Increases damage a 5"
        self.assertEqual(actual_data, expected_data)

    @patch('builtins.open', new_callable=mock_open, read_data='{"Green Wand": {"type": "weapon", "max_level": 3, "levels": [{"damage": 5}, {"area_of_effect": 0.1}, {"reload_time": -500}]}}')
    def test_max_level_property(self, mock_file):
        """Test the max_level property."""
        upgrade = Upgrade("Green Wand")

        # One assertEqual to check the max level
        self.assertEqual(upgrade.max_level, 3)

    @patch('builtins.open', new_callable=mock_open, read_data='{"Green Wand": {"type": "weapon", "max_level": 3, "levels": [{"damage": 5}, {"area_of_effect": 0.1}, {"reload_time": -500}], "unlock_info": "Shoots at the nearest enemy."}}')
    def test_unlock_info(self, mock_file):
        """Test the unlock_info property."""
        upgrade = Upgrade("Green Wand")

        # One assertEqual to check the unlock info
        self.assertEqual(upgrade.unlock_info, "Shoots at the nearest enemy.")

if __name__ == '__main__':
    unittest.main()

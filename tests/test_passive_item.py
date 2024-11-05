import unittest
from business.weapons.passive_item import PassiveItem, PlayerStats, Upgrade
from unittest.mock import patch
class TestPassiveItem(unittest.TestCase):
    @patch.object(Upgrade, 'apply_upgrade', return_value=None)
    def test_equality(self, mock_file):
        """Test equality of PassiveItem objects."""
        item1 = PassiveItem("Damage Boost")
        item2 = PassiveItem("Damage Boost")
        self.assertTrue(item1 == item2)
    
    @patch.object(Upgrade, 'apply_upgrade', return_value=None)
    def test_empty_stats(self, mock_file):
        item1 = PassiveItem("Dama boost")
        self.assertEqual(item1.stats.armor,0)
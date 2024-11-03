import unittest
from business.weapons.passive_item import PassiveItem, PlayerStats
class TestPassiveItem(unittest.TestCase):
    def test_equality(self):
        """Test equality of PassiveItem objects."""
        item1 = PassiveItem("Damage Boost")
        item2 = PassiveItem("Damage Boost")
        self.assertTrue(item1 == item2)
    
    def test_empty_stats(self):
        item1 = PassiveItem("Dama boost")
        self.assertEqual(item1.stats.armor,0)
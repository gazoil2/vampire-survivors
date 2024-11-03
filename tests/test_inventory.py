import unittest
from unittest.mock import MagicMock, patch
from business.weapons.weapon import Weapon
from business.weapons.inventory import Inventory
from business.weapons.passive_item import PassiveItem
from business.weapons.exception import FullInventoryError, ItemNotFoundError, InvalidItemError
from business.weapons.factories.weapon_factory import WeaponFactory
from business.weapons.factories.passive_factory import PassiveItemFactory
from business.weapons.stats import ProjectileStatsMultiplier

class TestInventory(unittest.TestCase):

    def setUp(self):
        self.max_inventory_size = 5
        self.weapons = []
        self.passive_items = []
        self.inventory = Inventory(self.weapons, self.passive_items, self.max_inventory_size)

        # Prepare mock weapons and passive items
        self.mock_weapon = Weapon(ProjectileStatsMultiplier.get_empty_projectile_stats(), MagicMock(), "Test Weapon")
        self.mock_passive = PassiveItem("Test Passive")

    def test_add_weapon_to_inventory(self):
        self.inventory.add_item_to_inventory(self.mock_weapon)
        self.assertIn(self.mock_weapon, self.inventory._Inventory__weapons)

    def test_add_passive_item_to_inventory(self):
        self.inventory.add_item_to_inventory(self.mock_passive)
        self.assertIn(self.mock_passive, self.inventory._Inventory__passive_items)

    def test_full_inventory_error_on_weapon(self):
        self.inventory._Inventory__weapons = [WeaponFactory.get_green_wand() for _ in range(self.max_inventory_size)]
        with self.assertRaises(FullInventoryError):
            self.inventory.add_item_to_inventory(self.mock_weapon)

    def test_full_inventory_error_on_passive_item(self):
        self.inventory._Inventory__passive_items = [PassiveItemFactory.get_spinach() for _ in range(self.max_inventory_size)]
        with self.assertRaises(FullInventoryError):
            self.inventory.add_item_to_inventory(self.mock_passive)

    def test_invalid_item_error(self):
        with self.assertRaises(InvalidItemError):
            self.inventory.add_item_to_inventory("invalid_item")

    def test_upgrade_weapon(self):
        self.inventory.add_item_to_inventory(self.mock_weapon)
        self.mock_weapon.can_be_upgraded = MagicMock(return_value=True)
        self.mock_weapon.upgrade = MagicMock()
        
        self.inventory.upgrade_item(self.mock_weapon)
        self.mock_weapon.upgrade.assert_called_once()

    def test_upgrade_non_existing_weapon(self):
        with self.assertRaises(ItemNotFoundError):
            self.inventory.upgrade_item(self.mock_weapon)

    @patch.object(Weapon, 'get_next_level_data', return_value="Mocked Level Data")
    def test_possible_actions(self, mock_file):
        # Add some weapons and passive items
        self.inventory.add_item_to_inventory(self.mock_weapon)        
        possible_actions = self.inventory.get_possible_actions()
        self.assertGreater(len(possible_actions), 0)  # Expect some actions to be available

    def test_combined_stats(self):
        self.mock_passive = MagicMock(spec=PassiveItem)
        self.mock_passive.stats = ProjectileStatsMultiplier.get_empty_projectile_stats()
        self.inventory.add_item_to_inventory(self.mock_passive)
        combined_stats = self.inventory.get_combined_stats()
        self.assertIsNotNone(combined_stats)  # Ensure combined stats can be retrieved

if __name__ == '__main__':
    unittest.main()

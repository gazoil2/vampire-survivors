from typing import List
from business.weapons.stats import PlayerStats
from business.weapons.weapon import Weapon
from business.weapons.interfaces import IUpdatable, IPassiveItem
from business.weapons.passive_item import PassiveItem
from business.weapons.exception import InvalidItemError, FullInventoryError, ItemNotFoundError
from business.weapons.factories.weapon_factory import WeaponFactory
from business.weapons.factories.passive_factory import PassiveItemFactory
from business.upgrades.upgradestrategy import ActionStrategy
class Inventory(IUpdatable):
    def __init__(self, weapons : List[Weapon], boosters : List[IPassiveItem], maxsize=5 ) -> None:
        self.__weapons : List[Weapon] = weapons
        self.__passive_items : List[IPassiveItem] = boosters
        self.__max_size = maxsize
        self.__all_weapons : List[Weapon] = WeaponFactory.get_all_weapons()
        self.__all_passives : List[IPassiveItem] = PassiveItemFactory.get_all_passive_items()

    def get_combined_stats(self):
        final_stats = PlayerStats.get_empty_player_stats()
        for passive in self.__passive_items:
            final_stats += passive.stats 
        return final_stats

    def add_item_to_inventory(self, item : IPassiveItem | Weapon):
        if isinstance(item,Weapon):
            if len(self.__weapons) == self.__max_size:
                raise FullInventoryError
            self.__weapons.append(item)
        elif isinstance(item,PassiveItem):
            if len(self.__passive_items) == self.__max_size:
                raise FullInventoryError
            self.__passive_items.append(item)
        else:
            raise InvalidItemError(item)

    def upgrade_item(self, item: IPassiveItem | Weapon):
        """Upgrade an item in the inventory."""
        if isinstance(item, Weapon):
            for weapon in self.__weapons:
                if weapon == item:  # Assuming weapons are comparable (implement __eq__ in Weapon class)
                    if weapon.can_be_upgraded():
                        weapon.upgrade()  # Assuming the upgrade method modifies the weapon stats
                        return
            raise ItemNotFoundError(item)

        elif isinstance(item, PassiveItem):
            for passive in self.__passive_items:
                if passive == item:  # Assuming passive items are comparable
                    if passive.can_be_upgraded():
                        passive.upgrade()  # Assuming the upgrade method modifies the passive item stats
                        return
            raise ItemNotFoundError(item)
        else:
            raise InvalidItemError(item)
    def update(self, world):
        for weapon in self.__weapons:
            weapon.update(world)
    
    def __get_possible_weapon_upgrades(self) -> List[ActionStrategy]:
        upgrades = []
        for weapon in self.__weapons:
            if weapon.can_be_upgraded():
                upgrade_data = weapon.get_next_level_data()  # Get the upgrade data for the next level
                upgrades.append(ActionStrategy(
                    description=f"{upgrade_data} {weapon.name}",
                    action_function=lambda w=weapon: self.upgrade_item(w),
                    item_name=weapon.name
                ))
        return upgrades

    def __get_possible_passive_upgrades(self) -> List[ActionStrategy]:
        upgrades = []
        for passive in self.__passive_items:
            if passive.can_be_upgraded():
                upgrade_data = passive.get_unlock_info() # Assuming a similar method exists for passive items
                upgrades.append(ActionStrategy(
                    description=f" {upgrade_data} ",
                    action_function=lambda p=passive: self.upgrade_item(p),
                    item_name=passive.name
                ))
        return upgrades

    def __get_possible_weapons(self) -> List[ActionStrategy]:
        possible_weapons = []
        for weapon in self.__all_weapons:
            if weapon not in self.__weapons: 
                unlock_data = weapon.get_unlock_info()
                possible_weapons.append(ActionStrategy(
                    description=unlock_data,
                    action_function=lambda w=weapon: self.add_item_to_inventory(w),
                    item_name=weapon.name
                ))
        
        return possible_weapons

    def __get_possible_passives(self) -> List[ActionStrategy]:
        possible_passives = []
        for passive in self.__all_passives:
            if passive not in self.__passive_items:
                unlock_data = passive.get_unlock_info()
                possible_passives.append(ActionStrategy(
                    description=unlock_data,
                    action_function=lambda p=passive: self.add_item_to_inventory(p),
                    item_name=passive.name
                ))
        
        return possible_passives

    
    def get_possible_actions(self) -> List[ActionStrategy]:
        return self.__get_possible_passives() + self.__get_possible_weapons() + self.__get_possible_passive_upgrades() + self.__get_possible_weapon_upgrades()
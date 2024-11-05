import unittest
from unittest.mock import MagicMock, patch

from business.entities.interfaces import IDamageable, IHasPosition
from business.entities.monster import Monster, MonsterStats


class TestMonster(unittest.TestCase):
    def setUp(self):
        self.monster = Monster(5, 5, MagicMock(), MonsterStats(1,100,1,1,1),MagicMock())

    def test_attack(self):
        target_mock = MagicMock(spec=[IDamageable, IHasPosition])
        target_mock.health = 10
        target_mock.take_damage = MagicMock()
        self.monster.attack(target_mock)
        target_mock.take_damage.assert_called_once_with(self.monster.damage_amount)


    def test_attack_is_not_called_when_action_is_not_ready(self):
        target_mock = MagicMock(spec=[IDamageable, IHasPosition])
        target_mock.health = 10
        target_mock.take_damage = MagicMock()

        self.monster.attack(target_mock)

        cooldown_handler = self.monster._Monster__attacked_enemies.get(target_mock)

        with patch.object(cooldown_handler, 'is_action_ready', return_value=False):
            self.monster.attack(target_mock)

        target_mock.take_damage.assert_called_once_with(self.monster.damage_amount)

    def test_take_damage_reduces_health(self):
        self.monster.take_damage(30)
        self.assertEqual(self.monster.health, 70)
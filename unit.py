from __future__ import annotations
from abc import ABC, abstractmethod
from equipment import Equipment, Weapon, Armor
from classes import UnitClass
from random import randint
from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass):
        """ При инициализации класса Unit используем свойства класса UnitClass """

        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used = False

    @property
    def health_points(self):
        """ Возвращает аттрибут hp (здоровье) в красивом виде """

        if self.hp < 0:
            return 0
        return round(self.hp, 1)

    @property
    def stamina_points(self):
        """ Возвращает аттрибут stamina (выносливость) в красивом виде. """

        if self.stamina < 0:
            return 0
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon):
        """ Присваивает герою новое оружие. """
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        """ Экипировка героя в новую броню. """
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> int:
        """ Возвращает предполагаемый урон для последующего вывода пользователю в текстовом виде """

        # Рассчитываем и уменьшаем выносливость игрока нападающего.
        self.stamina -= self.weapon.stamina_per_hit * self.unit_class.stamina

        # Расчет наносимого максимального урона.
        damage = self.weapon.damage * self.unit_class.attack

        # Проверяем сможет ли противник заблокировать удар (сколько стамины и расчет брони цели).
        if target.stamina > target.armor.stamina_per_turn * target.unit_class.stamina:
            target.stamina -= target.armor.stamina_per_turn * target.unit_class.stamina
            damage -= target.armor.defence * target.unit_class.armor

        return target.get_damage(damage)

    def get_damage(self, damage: int) -> Optional[int]:
        """ Возвращаем значение полученного урона целью
            и присваиваем новое значение для аттрибута self.h (кол-во здоровья) """
        if damage > 0:
            self.hp -= damage
            return round(damage, 1)
        return 0

    def use_skill(self, target: BaseUnit) -> str:
        """
            Метод использования умения.
            Если умение уже использовано возвращаем строку 'Навык использован'
            Иначе выполняем функцию, которая возвращает нам строку, характеризующая выполнение умения.
        """
        if self._is_skill_used:
            return 'Навык уже использован.'
        self._is_skill_used = True
        return self.unit_class.skill.use(user=self, target=target)

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
            Этот метод будет переопределен ниже
        """
        pass


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
            Функция удар игрока:
            здесь происходит проверка достаточно ли выносливости для нанесения удара.
            Вызывается функция подсчета наносимого урона self._count_damage(target).
        """
        if self.stamina * self.unit_class.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, " \
                   f"но у него не хватило выносливости."

        damage = self._count_damage(target)
        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника " \
                   f"и наносит {damage} урона."

        return f"{self.name} используя {self.weapon.name} наносит удар, " \
               f"но {target.armor.name} cоперника его останавливает."


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
            Функция удар соперника: содержит логику применения соперником умения
            (он должен делать это автоматически и только 1 раз за бой).
            Если умение не применено, противник наносит простой удар
        """

        if not self._is_skill_used and self.stamina >= self.unit_class.skill.stamina and randint(0, 100) < 10:
            return self.use_skill(target)

        if self.stamina * self.unit_class.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, " \
                   f"но у него не хватило выносливости."

        damage = self._count_damage(target)
        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} " \
                   f"и наносит Вам {damage} урона."

        return f"{self.name} используя {self.weapon.name} наносит удар, " \
               f"но Ваш(а) {target.armor.name} его останавливает."



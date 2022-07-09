from unit import BaseUnit

class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False
    battle_result = None

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        """ НАЧАЛО ИГРЫ присваиваем экземпляру класса аттрибуты 'игрок' и 'противник' """

        self.player = player
        self.enemy = enemy
        self.game_is_running = True


    def _check_players_hp(self):
        """ Проверка здоровья игрока и врага и возвращение результата строкой. """

        if self.player.hp > 0 and self.enemy.hp > 0:
            return None

        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = 'Ничья'
        elif self.player.hp <= 0:
            self.battle_result = 'Игрок проиграл битву'
        elif self.enemy.hp <= 0:
            self.battle_result = 'Игрок выиграл битву'

        # Завершаем игру и выводим результат, если выше прошла какая-либо из проверок.
        return self._end_game()


    def _stamina_regeneration(self):
        """ Восстанавливает стамину (выносливость) игрока и врага с учетом максимально возможной стамины. """

        units = (self.player, self.enemy)
        for unit in units:
            if unit.stamina + self.STAMINA_PER_ROUND > unit.unit_class.max_stamina:
                unit.stamina = unit.unit_class.max_stamina
            else:
                unit.stamina += self.STAMINA_PER_ROUND

    def next_turn(self):
        """ Возвращает результат ответного удара врага
            либо результат по окончании игры (если кончилось здоровье у кого-то). """

        result = self._check_players_hp()
        if result is not None:
            return result

        if self.game_is_running:
            self._stamina_regeneration()
            return  self.enemy.hit(self.player)


    def _end_game(self):
        """ Очистка синглтона, остановка игры и функция возвращает результат. """

        self._instances = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self):
        """ Возвращает результат от удара игрока и запускает следующий ход. """

        result = self.player.hit(self.enemy)
        turn_res = self.next_turn()
        return f'{result}\n{turn_res}'

    def player_use_skill(self):
        """ Возвращает результат удара после использования умения, и включает след. ход. """

        result = self.player.use_skill(self.enemy)
        turn_res = self.next_turn()
        return f'{result} {turn_res}'

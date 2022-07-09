from flask import render_template, Flask, request, url_for
from werkzeug.utils import redirect

from base import Arena
from classes import unit_classes
from equipment import Equipment
from unit import PlayerUnit, EnemyUnit

app = Flask(__name__)

heroes = {}

arena = Arena()  # инициализируем класс арены


@app.route("/")
def menu_page():
    """ Рендерим главное меню. """

    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    """ Выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы.
        Рендерим экран боя. """

    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])

    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    """ Если игра идет - происходит нанесение удара,
        иначе завершается игра и выводится результат. """

    if arena.game_is_running:
        result = arena.player_hit()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
    """ Кнопка использования скилла. Вызываем функцию использования скилла (arena.player_use_skill()). """

    if arena.game_is_running:
        result = arena.player_use_skill()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    """ Кнопка пропус хода. Вызываем здесь функцию следующий ход (arena.next_turn()). """

    if arena.game_is_running:
        result = arena.next_turn()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    """ Кнопка завершить игру - переход в главное меню. """

    return render_template("index.html", heroes=heroes)


@app.get("/choose-hero/")
def choose_hero():
    """ Отрисовка формы выбора героя. """

    result = {
        'classes': unit_classes,
        'weapons': Equipment().get_weapons_names(),
        'armors': Equipment().get_armors_names(),
        'header': 'Выберите героя'
    }

    return render_template('hero_choosing.html', result=result)


@app.post("/choose-hero/")
def choose_hero_post():
    """ Отправляем форму выбор героя и делаем редирект на эндпоинт choose enemy. """

    name = request.form['name']
    armor_name = request.form['armor']
    weapon_name = request.form['weapon']
    unit_class = request.form['unit_class']

    player = PlayerUnit(
        name=name,
        unit_class=unit_classes.get(unit_class)
    )

    player.equip_weapon(Equipment().get_weapon(weapon_name))
    player.equip_armor(Equipment().get_armor(armor_name))
    heroes['player'] = player

    return redirect(url_for('choose_enemy'))


@app.get("/choose-enemy/")
def choose_enemy():
    """ Отрисовка формы выбора противника. """

    result = {
        'classes': unit_classes,
        'weapons': Equipment().get_weapons_names(),
        'armors': Equipment().get_armors_names(),
        'header': 'Выберите врага'
    }

    return render_template('hero_choosing.html', result=result)


@app.post("/choose-enemy/")
def choose_enemy_post():
    """ Отправляем форму выбор противника и делаем редирект на начало битвы. """

    name = request.form['name']
    armor_name = request.form['armor']
    weapon_name = request.form['weapon']
    unit_class = request.form['unit_class']

    enemy = EnemyUnit(
        name=name,
        unit_class=unit_classes.get(unit_class)
    )

    enemy.equip_weapon(Equipment().get_weapon(weapon_name))
    enemy.equip_armor(Equipment().get_armor(armor_name))
    heroes['enemy'] = enemy

    return redirect(url_for('start_fight'))


if __name__ == "__main__":
    app.run()

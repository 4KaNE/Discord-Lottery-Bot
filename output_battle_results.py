import json
import random

# loading table
table_data = {}
try:
    with open('./output_battle_table.json', 'r', encoding="utf-8_sig") as fc:
        table_data = json.load(fc)
except json.JSONDecodeError as e:
    print('JSONDecodeError: ', e)
    exit(e)
except FileNotFoundError as e:
    print('FileNotFoundError: ', e)
    exit(e)


# get my tier
def get_tier(damage):
    loop_counter = 0
    while loop_counter < 100:
        loop_counter += 1    # 無限ループ防止用
        x = random.choice(table_data['tiers'])
        tier_min = int(x['min'])
        tier_max = int(x['max'])
        if tier_min <= damage <= tier_max:
            my_tier = int(x['tier'])
            n = random.choice([1, 2, 3])
            if n == 1:
                enemy_min_tier = int(x['1_min'])
                enemy_max_tier = int(x['1_max'])
            elif n == 2:
                enemy_min_tier = int(x['2_min'])
                enemy_max_tier = int(x['2_max'])
            else:
                enemy_min_tier = int(x['3_min'])
                enemy_max_tier = int(x['3_max'])
            return my_tier, enemy_min_tier, enemy_max_tier


# get my ship
def get_my_ship(tier):
    ships = []
    for x in table_data['ships']:
        if tier == int(x['tier']):
            ships.append(x['name'])
    return random.choice(ships)


# get enemy ships
def get_enemy_ships(min_tier, max_tier):
    enemy_cv_ships = []
    enemy_ships = []
    loop_counter = 0
    while len(enemy_ships) < 12 and loop_counter < 1000:
        loop_counter += 1    # 無限ループ防止用
        x = random.choice(table_data['ships'])
        kind = x['kind']
        if kind == '空母':
            if len(enemy_cv_ships) > 0:
                # 当面空母は１隻限定
                continue
        tier = int(x['tier'])
        if min_tier <= tier <= max_tier:
            if kind == '空母':
                enemy_cv_ships.append(x)
            enemy_ships.append(x)
    return enemy_ships


class ShipDamageClass:
    def __init__(self):
        self.name = ''
        self.hp_total = 0
        self.hp_remains = 0
        self.damage = 0
        self.sink = ''


# get damage results
def get_damage_results(damage, enemy_ships):
    remains = int(damage)
    pers = list(range(1, 100))
    target_ships = []
    target_ships_hp_total = 0
    for ship in enemy_ships:
        x = ShipDamageClass()
        x.name = ship['name']
        x.hp_total = round(int(ship['hp']) + int(ship['hp_add']))
        x.hp_remains = x.hp_total
        x.damage = 0
        target_ships.append(x)
        target_ships_hp_total += x.hp_total

    if target_ships_hp_total < remains:
        return ' 敵艦全滅(' + str(target_ships_hp_total) + ')以上のダメージを叩き出しました。神かよ'

    loop_counter = 0
    while remains > 0 and loop_counter < 100:
        loop_counter += 1    # 無限ループ防止用
        x = random.choice(target_ships)
        if x.hp_remains < 0:
            continue

        per_hp = random.choice(pers)
        ship_damage = round(x.hp_total * per_hp / 100)
        if x.hp_remains < ship_damage:
            ship_damage = x.hp_remains
        if remains < ship_damage:
            ship_damage = remains

        x.damage += ship_damage
        x.hp_remains -= ship_damage
        remains -= ship_damage

        n = random.choice(pers)
        if n <= 10:
            # 攻撃１回につき10%の確率で撃沈
            x.sink = '撃沈'

    damage_ships = []
    for x in target_ships:
        if x.damage > 0:
            s = x.name + x.sink + '(' + "{:,}".format(x.damage) + ')'
            damage_ships.append(s)

    return '、'.join(damage_ships)


# output_battle_results
def output_battle_results(damage):
    tiers = get_tier(damage)
    my_tier = tiers[0]
    enemy_min_tier = tiers[1]
    enemy_max_tier = tiers[2]
    my_ship = get_my_ship(my_tier)
    enemy_ships = get_enemy_ships(enemy_min_tier, enemy_max_tier)
    damage_result = get_damage_results(damage, enemy_ships)
    result = 'あなたの使用艦艇は' + my_ship + 'で、戦果は' + damage_result + 'でした。'

    return result

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
def get_my_tier(damage):
    while 1 == 1:
        x = random.choice(table_data['tiers'])
        tier_min = int(x['min'])
        tier_max = int(x['max'])
        if tier_min <= damage <= tier_max:
            return x['tier']


# get my ship
def get_my_ship(tier):
    ships = []
    for x in table_data['ships']:
        if tier == x['tier']:
            ships.append(x['name'])
    return random.choice(ships)


# get enemy tier
def get_enemy_tier(tier):
    out_min_tier = 0
    out_max_tier = 0
    if tier == '1':
        out_min_tier = 1
        out_max_tier = 1
    elif tier == '2':
        n = random.choice([0, 1])
        if n == 0:
            out_min_tier = 2
            out_max_tier = 2
        else:
            out_min_tier = 2
            out_max_tier = 3
    elif tier == '3':
        n = random.choice([0, 1])
        if n == 0:
            out_min_tier = 2
            out_max_tier = 3
        else:
            out_min_tier = 3
            out_max_tier = 4
    elif tier == '4':
        n = random.choice([0, 1])
        if n == 0:
            out_min_tier = 3
            out_max_tier = 4
        else:
            out_min_tier = 4
            out_max_tier = 5
    elif tier == '5':
        n = random.choice([0, 1, 2])
        if n == 0:
            out_min_tier = 4
            out_max_tier = 5
        elif n == 1:
            out_min_tier = 5
            out_max_tier = 6
        else:
            out_min_tier = 5
            out_max_tier = 7
    elif tier == '6':
        n = random.choice([0, 1, 2])
        if n == 0:
            out_min_tier = 4
            out_max_tier = 6
        elif n == 1:
            out_min_tier = 5
            out_max_tier = 7
        else:
            out_min_tier = 6
            out_max_tier = 8
    elif tier == '7':
        n = random.choice([0, 1, 2])
        if n == 0:
            out_min_tier = 5
            out_max_tier = 7
        elif n == 1:
            out_min_tier = 6
            out_max_tier = 8
        else:
            out_min_tier = 7
            out_max_tier = 9
    elif tier == '8':
        n = random.choice([0, 1, 2])
        if n == 0:
            out_min_tier = 6
            out_max_tier = 8
        elif n == 1:
            out_min_tier = 7
            out_max_tier = 9
        else:
            out_min_tier = 8
            out_max_tier = 10
    elif tier == '9':
        n = random.choice([0, 1])
        if n == 0:
            out_min_tier = 7
            out_max_tier = 9
        else:
            out_min_tier = 8
            out_max_tier = 10
    elif tier == '10':
        n = random.choice([0, 1])
        if n == 0:
            out_min_tier = 8
            out_max_tier = 10
        else:
            out_min_tier = 10
            out_max_tier = 10
    return out_min_tier, out_max_tier


# get damage results
def get_damage_results(damage, min_tier, max_tier):
    remains = int(damage)
    enemy_ships = []
    pers = list(range(1, 100))

    while remains > 0:
        x = random.choice(table_data['ships'])
        tier = int(x['tier'])
        if min_tier <= tier <= max_tier:
            per_hp_add = random.choice(pers)
            per_hp_damage = random.choice(pers)
            ship_hp = int(x['hp'])
            ship_hp_add = round(int(x['hp_add']) * per_hp_add / 100)
            ship_damage = round((ship_hp + ship_hp_add) * per_hp_damage / 100)

            remains -= ship_damage
            ship = x['name']
            n = random.choice(list(range(1, 100)))
            if n <= 10:
                ship += '撃沈'
            ship += '(' + "{:,}".format(ship_damage) + ')'

            enemy_ships.append(ship)
    return '、'.join(enemy_ships)


# output_battle_results
def output_battle_results(damage):
    my_tier = get_my_tier(damage)
    my_ship = get_my_ship(my_tier)
    enemy_tiers = get_enemy_tier(my_tier)
    enemy_min_tier = enemy_tiers[0]
    enemy_max_tier = enemy_tiers[1]
    damage_result = get_damage_results(damage, enemy_min_tier, enemy_max_tier)
    result = 'あなたの使用艦艇は' + my_ship + 'で、戦果は' + damage_result + 'でした。'

    return result

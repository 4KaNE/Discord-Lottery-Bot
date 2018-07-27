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
    while 1 == 1:
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
    enemy_ships = []
    while len(enemy_ships) < 12:
        x = random.choice(table_data['ships'])
        tier = int(x['tier'])
        if min_tier <= tier <= max_tier:
            enemy_ships.append(x)
    return enemy_ships


# get damage results
def get_damage_results(damage, enemy_ships):
    remains = int(damage)
    damage_ships = []
    pers = list(range(25, 100))

    while remains > 0:
        x = random.choice(enemy_ships)
        per_hp = random.choice(pers)
        ship_damage = round((int(x['hp']) + int(x['hp_add'])) * per_hp / 100)
        if remains < ship_damage:
            ship_damage = remains
        remains -= ship_damage
        ship = x['name']
        n = random.choice(list(range(1, 100)))
        if n <= 10:
            ship += '撃沈'
        ship += '(' + "{:,}".format(ship_damage) + ')'

        damage_ships.append(ship)
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

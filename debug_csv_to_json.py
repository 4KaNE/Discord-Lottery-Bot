import json
import csv
import codecs

json_data = {}

# tier_table.csvの読み込み
json_list = []
with open('d:/Python/tier_table.csv', 'r') as f:
    # list of dictの作成
    for line in csv.DictReader(f):
        json_list.append(line)

    # data check
    for x in json_list:
        if 1 > int(x['tier']) or int(x['tier']) > 10:
            raise ValueError("tier error!")
        if 0 > int(x['min']):
            raise ValueError("min error!")
        if 0 > int(x['max']):
            raise ValueError("max error!")

    # 範囲check
    max_value = 0
    for x in sorted(json_list, key=lambda m: int(m['min'])):
        if 0 <= int(x['min']) <= max_value + 1:
            max_value = max(max_value, int(x['max']))
        else:
            raise ValueError("min max error!")
    if max_value < 300000:
        raise ValueError("max error!")

    json_data["tiers"] = json_list

# ship_table.csvの読み込み
json_list = []
with open('d:/Python/ship_table.csv', 'r') as f:
    # list of dictの作成
    for line in csv.DictReader(f):
        json_list.append(line)

    # data check
    for x in json_list:
        x['hp_add'] = round(float(x['hp_add']))
        if 0 == len(x['nation']):
            raise ValueError("nation error!")
        if 1 > int(x['tier']) or int(x['tier']) > 10:
            raise ValueError("tier error!")
        if 0 == len(x['kind']):
            raise ValueError("kind error!")
        if 0 == len(x['name']):
            raise ValueError("name error!")
        if 1 > int(x['hp']) or int(x['hp']) > 110000:
            raise ValueError("hp error!")
        if 0 > int(x['hp_add']) or int(x['hp_add']) > 200000:
            raise ValueError("hp_add error!")

    json_data["ships"] = json_list

# output_battle_table.jsonへの出力
with codecs.open('./output_battle_table.json', 'w', encoding="utf-8_sig") as f:
    # JSONへの書き込み
    json.dump(json_data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))



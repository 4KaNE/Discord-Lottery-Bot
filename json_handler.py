"""This is a module which handles jsonfile"""
import json
import datetime

class JsonHandler():
    """jsonファイルの読み書きを行うクラス
    """
    def __init__(self):
        self.json_file = 'userData.json'

    def set_ign(self, discord_id, ign):
        """ignとDiscordIdを紐付して保存
           discordのユーザーIDがkey, ignがvalue
        """
        dump = True
        try:
            with open(self.json_file, 'r') as json_file:
                json_data = json.load(json_file)
            json_data["IGN"][discord_id] = ign
            with open(self.json_file, 'w') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4,\
                sort_keys=True, separators=(',', ': '))

        except json.decoder.JSONDecodeError:
            now = datetime.datetime.now()
            print("set_ignエラー:JSONDecodeError\n({}:{}) [{}]"\
            .format(discord_id, ign, now))
            dump = False

        return dump


    def add_result(self, discord_id, result):
        """くじの結果をjsonファイルに保存
           "result"{"IGN":{"日付":"くじの結果"}}
        """
        now = datetime.datetime.now()
        with open(self.json_file, 'r') as json_file:
            json_data = json.load(json_file)

        ign = json_data["IGN"][discord_id]
        if ign in json_data["result"]:
            json_data["result"][ign][now.date().strftime('%Y/%m/%d')] = result
        else:
            result_dict = {}
            result_dict[now.date().strftime('%Y/%m/%d')] = result
            json_data["result"][ign] = result_dict

        with open(self.json_file, 'w') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4,\
            sort_keys=True, separators=(',', ': '))


        return now.strftime('%m/%d %H:%M:%S')

    def check_today_result(self, discord_id):
        """今日のくじが引かれているかを調べる
           既にひかれている場合はresult=result, ひかれていない場合はresult = none
        """
        now = datetime.datetime.now()
        with open(self.json_file, 'r') as json_file:
            json_data = json.load(json_file)
        if str(discord_id) in json_data["IGN"]:
            has_ign = True
            ign = json_data["IGN"][discord_id]
            date_key = now.date().strftime('%Y/%m/%d')
            today_result = None
            if ign in json_data["result"] \
            and date_key in json_data["result"][ign]:
                today_result = json_data["result"][ign][date_key]

        else:
            has_ign = False
            today_result = None

        return has_ign, today_result


if __name__ == '__main__':
    JH = JsonHandler()
    JH.add_result("318549339544879106", "2599")

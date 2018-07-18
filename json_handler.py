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
            json_data = self._open_json()
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
           "Lottery_results":{"IGN":{"日付":"くじの結果"}}
        """
        now = datetime.datetime.now()
        json_data = self._open_json()
        ign = json_data["IGN"][discord_id]
        date_dict = {}
        date_dict["result"] = result
        date_dict["time"] = now.time().strftime('%H:%M:%S')
        if ign in json_data["Lottery_results"]:
            json_data["Lottery_results"][ign][now.date().strftime('%Y/%m/%d')] = date_dict
        else:
            result_dict = {}
            result_dict[now.date().strftime('%Y/%m/%d')] = date_dict
            json_data["Lottery_results"][ign] = result_dict

        with open(self.json_file, 'w') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4,\
            sort_keys=True, separators=(',', ': '))

        return now.strftime('%m/%d %H:%M:%S')

    def check_today_result(self, discord_id):
        """今日のくじが引かれているかを調べる
           既にひかれている場合はresult=result, ひかれていない場合はresult = none
        """
        now = datetime.datetime.now()
        ign = self._check_ign(discord_id)
        has_ign = False
        today_result = None
        if ign is not None:
            has_ign = True
            json_data = self._open_json()
            if ign in json_data["Lottery_results"]:
                datetime_key = now.date().strftime('%Y/%m/%d')
                if datetime_key in json_data["Lottery_results"][ign]:
                    today_result = json_data["Lottery_results"][ign][datetime_key]["result"]

        return has_ign, today_result

    def _check_ign(self, discord_id):
        """渡されたDiscordIdをキーに保存されたIGNが存在するか調べる
           戻り値はhas_ign = boolean, ign = (str or none)
        """
        with open(self.json_file, 'r') as json_file:
            json_data = json.load(json_file)
        if str(discord_id) in json_data["IGN"]:
            ign = json_data["IGN"][discord_id]
        else:
            ign = None

        return ign

    def _open_json(self):
        """jsonファイルを開いてdict型で返す
        """
        with open(self.json_file, 'r') as json_file:
            json_data = json.load(json_file)

        return json_data

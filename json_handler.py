"""This is a discord-lottery-Bot's module that handles json file"""
import json
import datetime

class JsonHandler():
    """Class to read and write json file.
    """
    def __init__(self):
        self.json_file = 'userData.json'

    def set_ign(self, discord_id, ign):
        """Save IGN with DiscordId.
           Key: DiscordId ,Value: IGN
           Return value:
               dump = boolean
        """
        json_data = self._open_json()

        if discord_id in json_data["IGN"]:
            change = True
            former_ign = json_data["IGN"][discord_id]
            if former_ign in json_data["Lottery_results"]:
                user_result = json_data["Lottery_results"][former_ign]
                del json_data["Lottery_results"][former_ign]
                json_data["Lottery_results"][ign] = user_result

        else:
            change = False

        json_data["IGN"][discord_id] = ign
        with open(self.json_file, 'w') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4,\
            sort_keys=True, separators=(',', ': '))

        return change


    def add_result(self, discord_id, result):
        """Save lottery result in json file.
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

    def add_ranking(self, discord_id, result):
        """Save the top 20 data in the json file.
        """
        pass

    def check_today_result(self, discord_id):
        """Confirm whether today's lottery result is saved or not.
           Return value:
               has_ign = boolean
               If already saved result=result, if not result = none
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
                    today_result = json_data["Lottery_results"][ign]\
                                            [datetime_key]["result"]

        return has_ign, today_result

    def calc_previous_day_stats(self):
        """Calculate statistics of the previous day
            Return pd_stats_dict
                pd_stats_dict = {
                    "pd_date": "2018/7/22",
                    "players": 50,
                    "first": {
                        "id": "xxxxxxxxxxxxxxxxxx",
                        "result": 300000
                    },
                    "second": {
                        "id": "xxxxxxxxxxxxxxxxxx",
                        "result": 250000
                    },
                    "third": {
                        "id": "xxxxxxxxxxxxxxxxxx",
                        "result": 200000
                    },
                    "fourth": {
                        "id": "xxxxxxxxxxxxxxxxxx",
                        "result": 150000
                    },
                    "fifth": {
                        "id": "xxxxxxxxxxxxxxxxxx",
                        "result": 100000
                    }
                }
        """
        pd_stats_dict = {}
        pd_key = "2018/07/22"
        pd_stats_dict["pd_date"] = pd_key
        pd_result_dict = {}
        json_data = self._open_json()
        for ign in json_data["Lottery_results"].keys():
            pd_userdata = json_data["Lottery_results"][ign].get(pd_key)
            if pd_userdata is not None:
                pd_result_dict[ign] = pd_userdata["result"]

        pd_result_list = pd_result_dict.values()
        pd_result_list = list(pd_result_list)
        pd_stats_dict["players"] = len(pd_result_list)
        pd_result_list = list(set(pd_result_list))#重複要素の削除
        pd_result_list.sort()
        pd_result_list.reverse()#数値が大きい順
        
        count = 0
        while count < 5:
            result_value = pd_result_list[count]
            result_keys = [k for k, v in pd_result_dict.items() if v == result_value]
            for result_ign in result_keys:
                count += 1
                user_dict = {}
                user_dict["id"] = self._check_discord_id(result_ign)
                user_dict["result"] = result_value
                if count == 1:
                    pd_stats_dict["first"] = user_dict
                elif count == 2:
                    pd_stats_dict["second"] = user_dict
                elif count == 3:
                    pd_stats_dict["third"] = user_dict
                elif count == 4:
                    pd_stats_dict["fourth"] = user_dict
                elif count == 5:
                    pd_stats_dict["fifth"] = user_dict

        return pd_stats_dict

    def _check_ign(self, discord_id):
        """Check if IGN is saved with discordId.
           Return value:
               ign = (str or None)
        """
        with open(self.json_file, 'r') as json_file:
            json_data = json.load(json_file)
        if str(discord_id) in json_data["IGN"]:
            ign = json_data["IGN"][discord_id]
        else:
            ign = None

        return ign

    def _check_discord_id(self, ign):
        """Return discordId from ign
        """
        json_data = self._open_json()
        try:
            discord_id = [k for k, v in json_data["IGN"].items() if v == ign][0]
        except IndexError:
            discord_id = None
        
        return discord_id
        


    def _open_json(self):
        """Open json file and return it as dict type.
        """
        with open(self.json_file, 'r') as json_file:
            try:
                json_data = json.load(json_file)
            except json.decoder.JSONDecodeError as error:
                print("Error occurred")
                print("type:" + str(type(error)))
                print("args:" + str(error.args))

        return json_data

if __name__ == '__main__':
    JH = JsonHandler()
    print(JH._check_discord_id("Akane_Kotonoha"))

"""This is a discord-lottery-Bot's module that handles json file"""
import json
import datetime

class JsonHandler():
    """
    Class to read and write json file.
    """
    def __init__(self):
        self.json_file = 'userData.json'
        self.first_day = datetime.datetime.strptime('2018/7/20', '%Y/%m/%d') 
        self.last_day = datetime.datetime.strptime('2018/7/28', '%Y/%m/%d')

    def set_ign(self, discord_id : str, ign : str) -> bool:
        """
        Save IGN with DiscordId.
        
        Parameters
        ----------
        discord_id : str
            User's discord id
        ign : str
            User's wows IGN
        
        Return
        ----------
        change : bool
            Whether or not it is already stored id.
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
                    "days_left",
                    "first": {
                        "id": "xxxxxxxxxxxxxxxxxx",
                        "result": 300000
                    }
                    2nd3rd4th5th}
        """
        pd_stats_dict = {}
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=1)
        pd_key = yesterday.strftime('%Y/%m/%d') 
        pd_stats_dict["pd_date"] = pd_key
        days_left = (self.last_day - now).days + 1
        pd_stats_dict["days_left"] = days_left
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
                else:
                    pass

        return pd_stats_dict

    def period_stats(self):
        """Infomation statistics of the event period
            Return period_stats_dict
                period_stats_dict = {
                    "players": 50,
                    "number_of_lotteries": 
                    "first": {
                        "id": "xxxxxxxxxxxxxxxxxx",
                        "result": 300000
                    }
                    2nd3rd4th5th}
        """
        period_stats_dict = {}
        result_list = []
        result_dict = {}
        date_key_list = ["2018/07/22", "2018/07/23", "2018/07/24", "2018/07/25", "2018/07/26", "2018/07/27"]
        json_data = self._open_json()
        period_stats_dict["players"] = len(json_data["Lottery_results"])
        for ign in json_data["Lottery_results"].keys():
            for date_key in date_key_list:
                date_userdata = json_data["Lottery_results"][ign].get(date_key)
                if date_userdata is not None:
                    result_list.append(date_userdata["result"])
                    if str(date_userdata["result"]) in result_dict:
                        ign_list = result_dict[str(date_userdata["result"])]
                        ign_list.append(ign)
                        result_dict[str(date_userdata["result"])] = ign_list
                        print("重複", date_userdata["result"])
                    else:
                        ign_list = []
                        ign_list.append(ign)
                        result_dict[str(date_userdata["result"])] = ign_list
        
        period_stats_dict["number_of_lotteries"] = len(result_list)
        result_list = list(set(result_list))
        result_list.sort()
        result_list.reverse()

        count = 0
        while count < 5:
            result_key = result_list[count]
            for result_ign in result_dict[str(result_key)]:
                count += 1
                user_dict = {}
                user_dict["id"] = self._check_discord_id(result_ign)
                user_dict["result"] = result_key
                if count == 1:
                    period_stats_dict["first"] = user_dict
                elif count == 2:
                    period_stats_dict["second"] = user_dict
                elif count == 3:
                    period_stats_dict["third"] = user_dict
                elif count == 4:
                    period_stats_dict["fourth"] = user_dict
                elif count == 5:
                    period_stats_dict["fifth"] = user_dict
                else:
                    pass

        return period_stats_dict

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
    print(JH.period_stats())

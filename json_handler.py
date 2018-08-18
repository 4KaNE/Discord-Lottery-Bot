"""This is a discord-lottery-Bot's module that handles json file"""
import json
import datetime
import time


class JsonHandler():
    """Class to read and write json file.
    """
    def __init__(self, logger, config):
        self.json_file = 'userData.json'
        self.logger = logger
        self.config = config
        self.first_day = self.config.kuji_first_day
        self.last_day = self.config.kuji_last_day

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
                    "days_left",
                    "ranks": [
                        [1
                         "xxxxxxxxxxxxxxxxxx",
                         300000]
                    ]
                    2nd3rd4th5th}
        """
        pd_stats_dict = {}
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=1)
        pd_key = yesterday.strftime('%Y/%m/%d')
        pd_stats_dict["pd_date"] = pd_key
        days_left = (self.last_day - now.date()).days + 1
        pd_stats_dict["days_left"] = days_left
        pd_result_list = []
        json_data = self._open_json()

        for ign in json_data["Lottery_results"].keys():
            pd_userdata = json_data["Lottery_results"][ign].get(pd_key)
            if pd_userdata is not None:
                # 昨日のIGNと値をdictに格納
                pd_result_list.append([ign, pd_userdata["result"], pd_userdata["time"]])

        pd_stats_dict["players"] = len(pd_result_list)
        pd_stats_dict["ranks"] = []

        # ランク順で昨日のデータを取得
        count = 0
        for v in sorted(pd_result_list, key=lambda x: (-x[1], x[2], x[0])):
            # ソート順確認
            self.logger.info(f"result={v[1]}、time={v[2]}、id={v[0]}")

            count += 1
            pd_stats_dict["ranks"].append([count, self._check_discord_id(v[0]), v[1]])

            if count >= self.config.rank_count:
                break

        return pd_stats_dict

    def period_stats(self):
        """Infomation statistics of the event period
            Return period_stats_dict
                period_stats_dict = {
                    "players": 50,
                    "number_of_lotteries": 
                    "ranks": [
                        [1
                         "xxxxxxxxxxxxxxxxxx",
                         300000]
                    ]
                    2nd3rd4th5th}
        """
        period_stats_dict = {}
        result_list = []
        date_key_list = self.config.kuji_days
        json_data = self._open_json()

        for ign in json_data["Lottery_results"].keys():
            for date_key in date_key_list:
                key = date_key.strftime('%Y/%m/%d')
                date_userdata = json_data["Lottery_results"][ign].get(key)
                if date_userdata is not None:
                    # 期間中のIGNと値と時刻をlistに格納
                    result_list.append([ign, date_userdata["result"], date_key, date_userdata["time"]])

        period_stats_dict["players"] = len(json_data["Lottery_results"])
        period_stats_dict["number_of_lotteries"] = len(result_list)
        period_stats_dict["ranks"] = []

        # ランク順で期間中のデータを取得
        count = 0
        for v in sorted(result_list, key=lambda x: (-x[1], x[2], x[3], x[0])):
            # ソート順確認
            self.logger.info(f"result={v[1]}、day={v[2]}、time={v[3]}、id={v[0]}")

            count += 1
            period_stats_dict["ranks"].append([count, self._check_discord_id(v[0]), v[1]])

            if count >= self.config.rank_count:
                break

        self.logger.info(period_stats_dict["ranks"])
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
    time.sleep(3000)

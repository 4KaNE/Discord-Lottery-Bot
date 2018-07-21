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

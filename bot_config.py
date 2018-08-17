import configparser
import datetime


class BotConfig:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('./setting.conf', encoding="utf-8_sig")
        self.bot_token = self.config['default']['bot_token']
        self.channel_id = self.config['default']['channel_id']
        self.command_set_ign = self.config['default']['command_set_ign'].split()
        self.command_kuji = self.config['default']['command_kuji'].split()
        self.kuji_first_day = datetime.datetime.strptime(self.config['default']['kuji_first_day'], '%Y/%m/%d')
        self.kuji_last_day = datetime.datetime.strptime(self.config['default']['kuji_last_day'], '%Y/%m/%d')
        self.kuji_days = []
        if self.kuji_first_day <= self.kuji_last_day:
            d = self.kuji_first_day
            delta = datetime.timedelta(days=1)
            while d <= self.kuji_last_day:
                self.kuji_days.append(d)
                d += delta

"""Botメインプログラム"""
import re
from numpy.random import randint
import discord
import json_handler

CLIENT = discord.Client()
JH = json_handler.JsonHandler()

@CLIENT.event
async def on_ready():
    """Bot起動確認
    """
    print("Bot start")

@CLIENT.event
async def on_message(message):
    """コメント監視
    """
    if message.content.startswith("!"):
        mention = "<@" + message.author.id + ">"
        if re.search("setIGN", message.content):
            split_content = message.content.split()
            if len(split_content) >= 2:
                dump = JH.set_ign(message.author.id, split_content[1])
                if dump is True:
                    res = "{} IGNを[{ign}]で登録しました。"\
                    .format(mention, ign=split_content[1])
                else:
                    res = "{} IGNの登録に失敗しました".format(mention)

            else:
                res = "{} IGNを判別できませんでした。入力に誤りがないか確認してください。\
                \n```!setIGN WoWs_In_Game_Name```".format(mention)

            await CLIENT.send_message(message.channel, res)

        elif re.search("kuji", message.content) \
          or re.search("kuzi", message.content):

            has_ign, today_result = JH.check_today_result(message.author.id)
            if has_ign is True:
                if today_result is None:
                    result = randint(1, 300001)
                    date = JH.add_result(message.author.id, result)
                    res = "{} 本日のくじを引きました！ [{}]\
                    \nあなたの与ダメージは{}です。".format(mention, date, result)

                else:
                    res = "{} 本日のくじはすでに引かれています!\
                    \nあなたの  与ダメージは{}です。".format(mention, today_result)

            else:
                res = "{} DiscordIDとIGNの紐づけが完了していません。先に\
                      \n```!setIGN WoWs_In_Game_Name```\
                      \nでIGNの登録をお願いします。".format(mention)


            await CLIENT.send_message(message.channel, res)


CLIENT.run("Token")

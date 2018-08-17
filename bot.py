"""Botメインプログラム"""
import asyncio
import re
import datetime

import aiohttp
from numpy.random import randint
import discord

import json_handler
import output_battle_results as OBR
import bot_config
import logging.config

# <editor-fold desc="setting">
logging.config.fileConfig("logging.conf")
logger = logging.getLogger()
config = bot_config.BotConfig()
CLIENT = discord.Client()
CHANNEL = discord.Object(id=config.channel_id)
JH = json_handler.JsonHandler(logger, config)
# </editor-fold>


@CLIENT.event
async def execute_regurary():
    """定期的に実行する処理
    """
    while True:
        now = datetime.datetime.now()
        if now.hour == 0 and now.minute == 0:
            pd_stats_dict = JH.calc_previous_day_stats()
            #メンションにしたいならmsgの先頭に@everyoneを追記
            msg = """
            \n{}の結果
            \nくじを引いたプレイヤー： {}人
            \n日別ランキングTop5
            \n1. <@{}> {}ダメージ
            \n2. <@{}> {}ダメージ
            \n3. <@{}> {}ダメージ
            \n4. <@{}> {}ダメージ
            \n5. <@{}> {}ダメージ
            \nイベント終了まで後{}日
            """.format(pd_stats_dict["pd_date"], pd_stats_dict["players"],\
            pd_stats_dict["first"]["id"], pd_stats_dict["first"]["result"],\
            pd_stats_dict["second"]["id"], pd_stats_dict["second"]["result"],\
            pd_stats_dict["third"]["id"], pd_stats_dict["third"]["result"],\
            pd_stats_dict["fourth"]["id"], pd_stats_dict["fourth"]["result"],\
            pd_stats_dict["fifth"]["id"], pd_stats_dict["fifth"]["result"],\
            pd_stats_dict["days_left"])

            try:
                await CLIENT.send_message(CHANNEL, msg)
            except discord.HTTPException:
                logger.error("送れなかった")
            except aiohttp.errors.ClientOSError:
                logger.error("接続失敗　ClientOSError")
            except asyncio.TimeoutError:
                logger.error("接続失敗　Timeout")

        await asyncio.sleep(60)


@CLIENT.event
async def on_ready():
    """Bot起動確認
    """
    print("Bot start")


@CLIENT.event
async def on_message(message):
    """コメント監視
    """
    if (message.author == CLIENT.user) or (message.channel.id != config.channel_id):
        # 自分自身の発言や、登録されていないチャンネルの発言は無視する。
        return

    mention = "<@" + message.author.id + ">"
    split_content = message.content.split()
    command = split_content[0]

    if command in config.command_set_ign:
        if len(split_content) >= 2:
            change = JH.set_ign(message.author.id, split_content[1])
            if change is True:
                res = "{} IGNを[{ign}]に変更しました！" \
                    .format(mention, ign=split_content[1])
            else:
                res = "{} IGNを[{ign}]で登録しました！" \
                    .format(mention, ign=split_content[1])

        else:
            res = "{} IGNを判別できませんでした。入力に誤りがないか確認してください。\
            \n```!setIGN WoWs_In_Game_Name```".format(mention)

        await CLIENT.send_message(message.channel, res)
        logger.info(res)

    elif command in config.command_kuji:
        has_ign, today_result = JH.check_today_result(message.author.id)
        if has_ign is True:
            if today_result is None:
                result = randint(1, 300001)
                date = JH.add_result(message.author.id, result)
                buttle_results = OBR.output_battle_results(result)
                res = "{} 本日のくじを引きました！ [{}]\
                \nあなたの与ダメージは{}です！\
                \n{}".format(mention, date, result, buttle_results)

            else:
                res = "{} 本日のくじはすでに引かれています!\
                \nあなたの与ダメージは{}です！".format(mention, today_result)

        else:
            res = "{} DiscordIDとIGNの紐づけが完了していません！先に\
                  \n```!setIGN WoWs_In_Game_Name```\
                  \nでIGNの登録をお願いします。".format(mention)

        await CLIENT.send_message(message.channel, res)
        logger.info(res)

CLIENT.loop.create_task(execute_regurary())
CLIENT.run(config.bot_token)

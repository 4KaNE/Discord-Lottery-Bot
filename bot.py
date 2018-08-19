"""Botメインプログラム"""
import asyncio
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


def command_previous_rank():
    pd_stats_dict = JH.calc_previous_day_stats()

    pd_date = pd_stats_dict["pd_date"]
    players = pd_stats_dict["players"]
    ranks = pd_stats_dict["ranks"]
    days_left = pd_stats_dict["days_left"]

    msg = (f"{pd_date}の結果\n"
           f"くじを引いたプレイヤー： {players}人\n"
           f"日別ランキングTop{config.rank_count}\n")

    for x in ranks:
        damage = "{:,}".format(x[2])
        msg += f"{x[0]}.<@{x[1]}> {damage}ダメージ\n"

    msg += f"イベント終了まで後{days_left}日"
    return msg


def command_rank():
    period_stats_dict = JH.period_stats()

    players = period_stats_dict["players"]
    number_of_lotteries = period_stats_dict["number_of_lotteries"]
    ranks = period_stats_dict["ranks"]
    first_day = config.kuji_first_day.strftime('%Y/%m/%d')
    last_day = config.kuji_last_day.strftime('%Y/%m/%d')

    msg = (f"イベント({first_day}～{last_day})の結果\n"
           f"くじを引いたプレイヤー： {players}人\n"
           f"くじが引かれた回数： {number_of_lotteries}回\n"
           f"ランキングTop{config.rank_count}\n")

    for x in ranks:
        damage = "{:,}".format(x[2])
        msg += f"{x[0]}.<@{x[1]}> {damage}ダメージ\n"

    return msg


@CLIENT.event
async def execute_regurary():
    """定期的に実行する処理
    """
    while True:
        now = datetime.datetime.now()
        if now.hour == 0 and now.minute == 0:
            if now.date() == config.kuji_first_day:
                command_kuji = "` または `".join(config.command_kuji)

                logger.info(config.command_set_ign)
                msg = (f"イベントスタートです!\n"
                       f"\n"
                       f"`{command_kuji}`とこのチャンネルに撃つことでランダムにダメージが入ります。\n"
                       f"くじの結果は日替わりで、同じ日に何度引いてもダメージは変わりません!\n"
                       f"\n"
                       f"また、イベントの参加には下記のコマンドでおふねのプレイヤーネーム登録が必要です。\n"
                       f"```{config.command_set_ign} WoWs_In_Game_Name```"
                       f"登録したプレイヤーネームは後から同じコマンドで変更することができます。")

            elif now.date() == (config.kuji_last_day + datetime.timedelta(days=1)):
                msg = command_rank()

            elif config.kuji_first_day < now.date() <= config.kuji_last_day:
                msg = command_previous_rank()
            else:
                msg = None

            if msg is not None:
                try:
                    logger.info(msg)
                    await CLIENT.send_message(CHANNEL, msg)
                except discord.HTTPException:
                    logger.error("送れなかった")
                except aiohttp.errors.ClientOSError:
                    logger.error("接続失敗　ClientOSError")
                except asyncio.TimeoutError:
                    logger.error("接続失敗　Timeout")

        wait = 60 - now.second
        await asyncio.sleep(wait)


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

    now = datetime.datetime.now()
    if command in config.command_help or \
            command in config.command_set_ign or \
            config.kuji_first_day <= now.date() <= config.kuji_last_day:
        pass
    else:
        first_day = config.kuji_first_day.strftime('%Y/%m/%d')
        last_day = config.kuji_last_day.strftime('%Y/%m/%d')
        res = f"イベント期間は{first_day}～{last_day}です。"
        await CLIENT.send_message(message.channel, res)
        logger.info(res)
        return

    if command in config.command_help:
        first_day = config.kuji_first_day.strftime('%Y/%m/%d')
        last_day = config.kuji_last_day.strftime('%Y/%m/%d')

        res = (f"イベント期間は{first_day}～{last_day}です。\n"
               f"くじを引く前に{config.command_set_ign}でIGNと紐づけてください。\n"
               f"くじの結果は日替わりで、同じ日に何度引いてもダメージは変わりません!\n"
               f"ランキングはダメージ降順、日時昇順、ID順となります。同じランクはありません。")

        await CLIENT.send_message(message.channel, res)
        logger.info(res)

    elif command in config.command_set_ign:
        res = None
        if len(split_content) >= 2:
            r = JH.set_ign(message.author.id, split_content[1])
            if r == json_handler.Status.UPDATE:
                res = "{} IGNを[{ign}]に変更しました！" \
                    .format(mention, ign=split_content[1])
            elif r == json_handler.Status.INSERT:
                res = "{} IGNを[{ign}]で登録しました！" \
                    .format(mention, ign=split_content[1])
            elif r == json_handler.Status.NO_UPDATE:
                res = "{} IGN[{ign}]は変更の必要がありません！" \
                    .format(mention, ign=split_content[1])
            elif r == json_handler.Status.IGN_KEY_ERROR:
                res = "{} IGN[{ign}]は既に使われています！" \
                    .format(mention, ign=split_content[1])
            elif r == json_handler.Status.EXCEPTION:
                res = "{} IGN[{ign}]の更新に失敗しました！" \
                    .format(mention, ign=split_content[1])
        if res is None:
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
                \n{}".format(mention, date, "{:,}".format(result), buttle_results)

            else:
                res = "{} 本日のくじはすでに引かれています!\
                \nあなたの与ダメージは{}です！".format(mention, "{:,}".format(today_result))

        else:
            res = "{} DiscordIDとIGNの紐づけが完了していません！先に\
                  \n```!setIGN WoWs_In_Game_Name```\
                  \nでIGNの登録をお願いします。".format(mention)

        await CLIENT.send_message(message.channel, res)
        logger.info(res)

    elif command in config.command_previous_rank:
        res = command_previous_rank()

        await CLIENT.send_message(message.channel, res)
        logger.info(res)

    elif command in config.command_rank:
        res = command_rank()

        await CLIENT.send_message(message.channel, res)
        logger.info(res)

CLIENT.loop.create_task(execute_regurary())

try:
    CLIENT.run(config.bot_token)
except Exception as e:
    logger.error(f'CLIENT.run Error:{e}')
    exit(e)
finally:
    logger.info(f'CLIENT.run end')

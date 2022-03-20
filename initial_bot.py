import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, SelectOption, Select
from wakeonlan import send_magic_packet
from twitchAPI.twitch import Twitch
import pandas as pd
import random
from dataclasses import dataclass  # simple structs
import datetime as dt
import config
import os

# DISCORD BOT SETUP
bot = commands.Bot(command_prefix='!')
DiscordComponents(bot)

# TWITCH CLIENT SETUP
client_id = config.TWITCH_CLIENT_ID
my_app_secret = config.TWITCH_CLIENT_SECRET
twitch = Twitch(client_id, my_app_secret)


@bot.command()
async def status(ctx):
    await ctx.send('Pi Bot: ONLINE')


@bot.command()
async def wake_d2(ctx):
    send_magic_packet('D0-50-99-A7-88-AE')
    await ctx.send('Waking D2')


@dataclass  # python struct functionality
class RateInfo:
    rating: int
    clip_use: str = "no"
    video_use: str = "no"
    clip_title: str = ""


def add_video(clip_info, rate_info):
    video_database = pd.read_csv(config.VIDEO_CSV, index_col=0)

    video_database.loc[clip_info["id"]] = {
        'video_title': clip_info["title"],
        'rating': rate_info.rating,
        'clip_use': rate_info.clip_use,
        'clip_title': rate_info.clip_title,
        'video_use': rate_info.video_use,
        'broadcaster_name': clip_info["broadcaster_name"],
        'broadcaster_id': clip_info["broadcaster_id"],
        'game_name': twitch.get_games([clip_info["game_id"]])["data"][0]["name"],
        'game_id': clip_info["game_id"],
        'video_url': clip_info["url"],
        'video_mp4': clip_info["thumbnail_url"].split("-preview")[0] + ".mp4",
        'thumbnail_jpg': clip_info["thumbnail_url"],
        'view_count': clip_info["view_count"],
        'time_created': clip_info["created_at"],  # might want to alter this (maybe turn into datetime)
        'duration': clip_info["duration"]
    }

    video_database.to_csv(config.VIDEO_CSV)


@bot.command()
async def video_test(ctx):
    for n in range(30):
        scrape_database = pd.read_csv(config.SCRAPE_CSV, index_col=0)

        clip = twitch.get_clips(clip_id=scrape_database.index[0])["data"][0]
        scrape_database.drop(index=scrape_database.index[0], axis=0, inplace=True)
        await ctx.send(".\n\n\n\n\n\n.")

        # INTRO ##########################################################################################
        if clip["duration"] > 50:
            url = clip["url"]
        else:
            url = clip["thumbnail_url"].split("-preview")[0] + ".mp4"

        message = ("Title: **" + clip["title"] + "**" +
                   "\nBroadcaster: **" + clip["broadcaster_name"] + "**" +
                   "\t\tGame: **" + twitch.get_games([clip["game_id"]])["data"][0]["name"] + "**\n" +
                   url)

        # RATING #########################################################################################
        rate_message = await ctx.send(message, components=[
            [Button(label="1"), Button(label="2"), Button(label="3"),
             Button(label="4"), Button(label="5")],
            [Button(label="6"), Button(label="7"), Button(label="8"),
             Button(label="9"), Button(label="10")],
            [Button(label="delete", style=4)]
        ])
        interaction_rate = await bot.wait_for("button_click")
        try:
            await interaction_rate.respond()
        except(Exception,):
            pass
        await rate_message.edit(components=[])
        await ctx.send(f"*Rated: **{interaction_rate.component.label}***. By {interaction_rate.author}")
        if interaction_rate.component.label == "delete":
            continue
        clip_rating = RateInfo(interaction_rate.component.label)

        # USE AS CLIP ####################################################################################
        clip_message = await ctx.send("Use as a **Clip**?", components=[
            [Button(label="yes", style=3), Button(label="no", style=4)]
        ])
        interaction_clip = await bot.wait_for("button_click")
        try:
            await interaction_clip.respond()
        except(Exception,):
            pass
        await clip_message.edit(components=[])

        # Clip Title #####################################################################################
        if interaction_clip.component.label == "yes":
            clip_rating.clip_use = "yes"
            await clip_message.edit(f"*Use as a Clip: **{interaction_clip.component.label}***." +
                                    f" By {interaction_clip.author}")

            await ctx.send("Enter Clip Name:")
            while True:
                msg = await bot.wait_for("message")

                title_message = await ctx.send(f"Confirm? ({msg.content})", components=[
                    [Button(label="yes", style=3), Button(label="no", style=4)]
                ])

                interaction_title = await bot.wait_for("button_click")
                try:
                    await interaction_title.respond()
                except(Exception,):
                    pass

                if interaction_title.component.label == "yes":
                    await title_message.edit(f"*Clip Title: **{msg.content}***", components=[])
                    clip_rating.clip_title = msg.content
                    break
                await title_message.delete()
        else:
            await clip_message.edit(f"*Use as a Clip: **{interaction_clip.component.label}***." +
                                    f" By {interaction_clip.author}")

        # Main Video #####################################################################################
        video_message = await ctx.send("Use in a **Video**?", components=[
            [Button(label="yes", style=3), Button(label="no", style=4)]
        ])
        interaction_video = await bot.wait_for("button_click")

        try:
            await interaction_video.respond()
        except(Exception,):
            pass

        clip_rating.video_use = interaction_video.component.label
        await video_message.edit(f"*Use in a Video: **{interaction_video.component.label}***." +
                                 f" By {interaction_video.author}", components=[])

        add_video(clip, clip_rating)
        scrape_database.to_csv(config.SCRAPE_CSV)


@bot.command()  # This will be a normal function
async def scrape_videos(ctx):
    # TODO Intelligent Video Scraping Process (BASED ON MY YT CHANNELS)

    scrape_database = pd.read_csv(config.SCRAPE_CSV, index_col=0)
    archive_database = pd.read_csv(config.ARCHIVE_CSV, index_col=0)

    month_ago = dt.datetime.now() - dt.timedelta(days=30)
    clips = twitch.get_clips(broadcaster_id="94753024", first=10, started_at=month_ago)

    for clip in clips["data"]:
        if clip["id"] not in archive_database.index:
            scrape_database.loc[clip["id"]] = [clip["broadcaster_id"],
                                               clip["game_id"],
                                               clip["created_at"],
                                               clip["view_count"]]
            archive_database.loc[clip["id"]] = [clip["url"]]
        else:
            pass  # print(clip['id'] + ": Duplicate")

    scrape_database.to_csv(config.SCRAPE_CSV)
    archive_database.to_csv(config.ARCHIVE_CSV)

    # TODO Automate: Dataframe for each channel? (I WILL PROBABLY MAKE THIS)

    # Future TODO Two programs: discord bot, twitch trend/activity monitor
    pass


@bot.command()
async def video_rated(ctx, *args):
    video_database = pd.read_csv(config.VIDEO_CSV, index_col=0)
    videos = video_database.loc[video_database['rating'] == int(args[0])]

    if videos.shape[0] != 0:
        random.seed(dt.datetime.now())
        index = random.randrange(videos.shape[0])
        video = videos.iloc[index]
        if video['duration'] < 55:
            url = video['video_mp4']
        else:
            url = video['video_url']
        message = ("Title: **" + video['video_title'] + "**" +
                   "\nBroadcaster: **" + video['broadcaster_name'] + "**" +
                   "\t\tGame: **" + video['game_name'] + "**\n" +
                   url)
        await ctx.send(message)
    else:
        await ctx.send(f"No videos rated {args[0]}")


def twitch_vid_test():

    # Adds any new games that have reached the current top 10
    game_database = pd.read_csv(config.GAMES_CSV, index_col=0)
    games = twitch.get_top_games(first=10)  # sorted by current active viewers
    for n in games["data"]:
        game = n
        if int(game["id"]) not in game_database.index:
            game_database.loc[game["id"]] = [game["name"]]
    game_database.to_csv(config.GAMES_CSV)

    # Adds any new casters that have reached the current top 15 clips
    caster_database = pd.read_csv(config.BROADCASTER_CSV, index_col=0)
    month_ago = dt.datetime.now() - dt.timedelta(days=30)
    clip_by_id = twitch.get_clips(game_id="509658", first=15, started_at=month_ago)
    for clip in clip_by_id["data"]:
        if int(clip["broadcaster_id"]) not in caster_database.index:
            print(clip["broadcaster_id"] + "," + clip["broadcaster_name"])
            # caster_database.loc[clip["broadcaster_id"]] = [clip["broadcaster_name"]]
    caster_database.to_csv(config.BROADCASTER_CSV)

# TO DO Function to fix outdated clip info (as needed?)


bot.run(config.DISCORD_TOKEN)

import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, SelectOption, Select
from twitchAPI.twitch import Twitch
import pandas as pd
import random
from dataclasses import dataclass  # simple structs
import datetime as dt
import config
import os

bot = commands.Bot(command_prefix='!')
DiscordComponents(bot)

client_id = config.TWITCH_CLIENT_ID
my_app_secret = config.TWITCH_CLIENT_SECRET
twitch = Twitch(client_id, my_app_secret)


@dataclass
class RateInfo:
    rating: int
    clip_use: str = "no"
    video_use: str = "no"
    clip_title: str = ""


def add_video(clip_info, rate_info, database='video_database.csv'):
    video_database = pd.read_csv(database, index_col=0)

    video_database.loc[clip_info["video_id"]] = {
        'id': clip_info["id"],
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

    video_database.to_csv(database)


@bot.command()
async def status(ctx):
    await ctx.send('Pi Bot: ONLINE')


@bot.command()
async def video_test(ctx):

    week_ago = dt.datetime.now() - dt.timedelta(days=7)
    # TODO Make database file for game/broadcaster ids

    # TODO Pull from raw clip database
    clips = twitch.get_clips(broadcaster_id="37402112", first=30, started_at=week_ago)

    # print(clips["data"][0])

    for n in range(30):
        clip = clips["data"][n]
        await ctx.send(".\n\n\n\n\n\n.")

        # TODO Edit database info at the start of editing to avoid duplicates

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


@bot.command()  # This will be a normal function
async def scrape_videos(ctx):
    month_ago = dt.datetime.now() - dt.timedelta(days=30)
    clips = twitch.get_clips(broadcaster_id="37402112", first=30, started_at=month_ago)

    # TODO Fill out games csv (games that are popular or that we want videos for)
    # TODO Fill out broadcaster csv (broadcasters that are popular or that we want videos of)

    # TODO Make Scrape Database

    # TODO Automate: Dataframe for each channel?

    # TODO Get Top Games (and check the usual)
    games = twitch.get_top_games()  # sorted by current active viewers
    print(games)

    # TODO Get Top Broadcasters (Not known: how to do this)

    # Initialize data to lists.
    data = clips["data"]

    # Creates DataFrame.
    df = pd.DataFrame(data)

    # Print the data
    print(df.iloc[0])
    print(df)

    # TODO Add mass amounts of videos to database (without duplicates)
    pass

# TO DO Function to fix outdated clip info (as needed?)


@bot.command()
async def video_rated(ctx, *args):
    video_database = pd.read_csv('video_database.csv', index_col=0)
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

bot.run(config.DISCORD_TOKEN)

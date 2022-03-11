import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, SelectOption, Select
from twitchAPI.twitch import Twitch
import pandas as pd
import datetime as dt
import config
import os

bot = commands.Bot(command_prefix='!')
DiscordComponents(bot)

client_id = config.TWITCH_CLIENT_ID
my_app_secret = config.TWITCH_CLIENT_SECRET
twitch = Twitch(client_id, my_app_secret)


@bot.command()
async def status(ctx):
    await ctx.send('Pi Bot: ONLINE')


@bot.command()
async def video_test(ctx):

    week_ago = dt.datetime.now() - dt.timedelta(days=7)
    # TODO Make database file for game/broadcaster ids
    clips = twitch.get_clips(broadcaster_id="37402112", first=30, started_at=week_ago)

    print(clips["data"][0])

    for n in range(30):
        await ctx.send(".\n\n\n\n\n\n.")

        # TODO Edit database info at the start of editing to avoid duplicates

        # INTRO ##########################################################################################
        if clips["data"][n]["duration"] > 50:
            message = ("Title: **" + clips["data"][n]["title"] + "**" +
                       "\nBroadcaster: **" + clips["data"][n]["broadcaster_name"] + "**" +
                       "\t\tGame: **" + twitch.get_games([clips["data"][n]["game_id"]])["data"][0]["name"] + "**\n" +
                       clips["data"][n]["url"])
        else:
            message = ("Title: **" + clips["data"][n]["title"] + "**" +
                       "\nBroadcaster: **" + clips["data"][n]["broadcaster_name"] + "**" +
                       "\t\tGame: **" + twitch.get_games([clips["data"][n]["game_id"]])["data"][0]["name"] + "**\n" +
                       clips["data"][n]["thumbnail_url"].split("-preview")[0] + ".mp4")

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

        # USE AS CLIP ####################################################################################
        clip_message = await ctx.send("Use as a **Clip**?", components=[
            [Button(label="Yes", style=3), Button(label="No", style=4)]
        ])
        interaction_clip = await bot.wait_for("button_click")
        try:
            await interaction_clip.respond()
        except(Exception,):
            pass
        await clip_message.edit(components=[])

        # Clip Title #####################################################################################
        if interaction_clip.component.label == "Yes":
            await clip_message.edit(f"*Use as a Clip: **{interaction_clip.component.label}***." +
                                    f" By {interaction_clip.author}")

            await ctx.send("Enter Clip Name:")
            while True:
                msg = await bot.wait_for("message")

                title_message = await ctx.send(f"Confirm? ({msg.content})", components=[
                    [Button(label="Yes", style=3), Button(label="No", style=4)]
                ])

                interaction_title = await bot.wait_for("button_click")
                try:
                    await interaction_title.respond()
                except(Exception,):
                    pass

                if interaction_title.component.label == "Yes":
                    await title_message.edit(f"*Clip Title: **{msg.content}***", components=[])
                    break
                await title_message.delete()
        else:
            await clip_message.edit(f"*Use as a Clip: **{interaction_clip.component.label}***." +
                                    f" By {interaction_clip.author}")

        # Main Video #####################################################################################
        video_message = await ctx.send("Use in a **Video**?", components=[
            [Button(label="Yes", style=3), Button(label="No", style=4)]
        ])
        interaction_video = await bot.wait_for("button_click")

        try:
            await interaction_video.respond()
        except(Exception,):
            pass

        await video_message.edit(f"*Use in a Video: **{interaction_video.component.label}***." +
                                 f" By {interaction_video.author}", components=[])

        # TODO Add info to pandas database


@bot.command()
async def scrape_videos(ctx):
    # TODO Add mass amounts of videos to database (without duplicates)
    pass


@bot.command()
async def add_video(ctx):
    # TODO Add an example video to a pandas database
    video_database = pd.read_csv('video_database.csv', index_col=0)
    clips = twitch.get_clips(broadcaster_id="37402112", first=2)
    clip = clips["data"][1]

    video_database.loc[clip["video_id"]] = {
        'id': clip["id"],
        'video_title': clip["title"],
        'rating': 5,  # example
        'clip_use': "yes",  # example
        'clip_title': "My First Example Video",  # example
        'video_use': "yes",  # example
        'broadcaster_name': clip["broadcaster_name"],
        'broadcaster_id': clip["broadcaster_id"],
        'game_name': twitch.get_games([clip["game_id"]])["data"][0]["name"],
        'game_id': clip["game_id"],
        'video_url': clip["url"],
        'video_mp4': clip["thumbnail_url"].split("-preview")[0] + ".mp4",
        'thumbnail_jpg': clip["thumbnail_url"],
        'view_count': clip["view_count"],
        'time_created': clip["created_at"],  # might want to alter this (maybe turn into datetime)
        'duration': clip["duration"]
    }

    video_database.to_csv('video_database.csv')

    # video ID?
    # id
    # title
    # rating
    # use as clip
    # clip title
    # use in video
    # broadcaster
    # broadcaster ID
    # game
    # game ID
    # url
    # video mp4
    # thumbnail url
    # view count
    # time created
    # duration
    # / language
    # / creator ID
    # / creator name
    # / embed url
    # None of these are negotiable
    # Some systems will use this data without the twitch api

# TO DO Function to fix outdated clip info


@bot.command()
async def video_rated(ctx, *args):
    # TODO Function to show clip of given rating (optional: broadcaster)
    print(args)

bot.run(config.DISCORD_TOKEN)

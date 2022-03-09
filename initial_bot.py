import discord
# from discord.ui import Button # Only in Discord.py 2.0 (requires python <3.7)
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, SelectOption, Select

import pandas as pd

from twitchAPI.twitch import Twitch

import config
import os

bot = commands.Bot(command_prefix='!')
DiscordComponents(bot)

client_id = config.TWITCH_CLIENT_ID
my_app_secret = config.TWITCH_CLIENT_SECRET

twitch = Twitch(client_id, my_app_secret)


import datetime as DT
today = DT.date.today()
week_ago = today - DT.timedelta(days=7)


@bot.command()
async def status(ctx):
    await ctx.send('Pi Bot: ONLINE')


@bot.command()
async def button(ctx):
    await ctx.send("hello", components=[
        [Button(label="1", style=2, custom_id="1"),
         Button(label="2", style=2, custom_id="2"),
         Button(label="3", style=2, custom_id="3"),
         Button(label="4", style=2, custom_id="4"),
         Button(label="5", style=2, custom_id="5")],
        [Button(label="6", style=2, custom_id="6"),
         Button(label="7", style=2, custom_id="7"),
         Button(label="8", style=2, custom_id="8"),
         Button(label="9", style=2, custom_id="9"),
         Button(label="10", style=2, custom_id="10")],
        [Button(label="Delete", style=4, custom_id="button_delete")]
    ])
    interaction = await bot.wait_for("button_click")
    try:
        await interaction.respond()
    except:
        pass
    await ctx.send("Success: " + interaction.component.label)


@bot.command()
async def video_test(ctx):
    clips = twitch.get_clips(broadcaster_id="37402112", first=30, started_at=DT.datetime(2021, 12, 6))

    for n in range(30):
        if clips["data"][n]["duration"] > 50:
            message = ("Title: **" + clips["data"][n]["title"] + "**\n" +
                           "Broadcaster: **" + clips["data"][n]["broadcaster_name"] + "**\n" +
                           clips["data"][n]["url"])
        else:
            message = ("Title: **" + clips["data"][n]["title"] + "**\n" +
                           "Broadcaster: **" + clips["data"][n]["broadcaster_name"] + "**\n" +
                           clips["data"][n]["thumbnail_url"].split("-preview")[0] + ".mp4")

        # RATING ##########################################################################################
        await ctx.send(message, components=[
            [Button(label="1", style=2, custom_id="1"),
             Button(label="2", style=2, custom_id="2"),
             Button(label="3", style=2, custom_id="3"),
             Button(label="4", style=2, custom_id="4"),
             Button(label="5", style=2, custom_id="5")],
            [Button(label="6", style=2, custom_id="6"),
             Button(label="7", style=2, custom_id="7"),
             Button(label="8", style=2, custom_id="8"),
             Button(label="9", style=2, custom_id="9"),
             Button(label="10", style=2, custom_id="10")],
            [Button(label="Delete", style=4, custom_id="button_delete")]
        ])
        interaction_rate = await bot.wait_for("button_click")
        try:
            await interaction_rate.respond()
        except:
            pass

        await ctx.send("Rated: " + interaction_rate.component.label)
        print(interaction_rate.component.label)

        # USE AS CLIP ####################################################################################
        await ctx.send("Use as a **clip**?", components=[
            [Button(label="Yes", style=3, custom_id="yes"),
             Button(label="No", style=4, custom_id="no")]
        ])
        interaction_clip = await bot.wait_for("button_click")
        try:
            await interaction_clip.respond()
        except:
            pass

        await ctx.send("Rated: " + interaction_clip.component.label)
        print(interaction_clip.component.label)


        await ctx.send("Done\n\n\n\n\n\nNext")


    # clip_number = 4
    # print(clips["data"][clip_number])
    # await ctx.send("title\n" + clips["data"][clip_number]["thumbnail_url"].split("-preview")[0] + ".mp4")
    # await ctx.send(clips["data"][clip_number]["url"])


@bot.command()
async def greet(ctx):
    await ctx.send("Say hello!")

    msg = await bot.wait_for("message")
    await ctx.send(f"Hello {msg.author}! ({msg.content})")

bot.run(config.DISCORD_TOKEN)

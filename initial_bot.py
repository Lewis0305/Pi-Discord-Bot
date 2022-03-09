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
        except:
            pass
        await rate_message.edit(components=[])
        await ctx.send(f"*Rated: **{interaction_rate.component.label}***. By {interaction_rate.author}")
        if interaction_rate.component.label == "delete":
            await ctx.send(".\n\n\n\n\n\n.")
            continue

        # USE AS CLIP ####################################################################################
        clip_message = await ctx.send("Use as a **Clip**?", components=[
            [Button(label="Yes", style=3), Button(label="No", style=4)]
        ])
        interaction_clip = await bot.wait_for("button_click")
        try:
            await interaction_clip.respond()
        except:
            pass
        await clip_message.edit(components=[])

        # Clip Title #####################################################################################
        if interaction_clip.component.label == "Yes":
            await clip_message.edit(f"*Use as a Clip: **{interaction_clip.component.label}***. By {interaction_clip.author}")

            await ctx.send("Enter Clip Name:")
            while True:
                msg = await bot.wait_for("message")

                title_message = await ctx.send(f"Confirm? ({msg.content})", components=[
                    [Button(label="Yes", style=3), Button(label="No", style=4)]
                ])

                interaction_title = await bot.wait_for("button_click")
                try:
                    await interaction_title.respond()
                except:
                    pass

                if interaction_title.component.label == "Yes":
                    await title_message.edit(f"*Clip Title: **{msg.content}***", components=[])
                    break
                await title_message.delete()
        else:
            await clip_message.edit(f"*Use as a Clip: **{interaction_clip.component.label}***. By {interaction_clip.author}")

        # Main Video #####################################################################################
        video_message = await ctx.send("Use in a **Video**?", components=[
            [Button(label="Yes", style=3), Button(label="No", style=4)]
        ])
        interaction_video = await bot.wait_for("button_click")
        try:
            await interaction_video.respond()
        except:
            pass

        await video_message.edit(f"*Use in a Video: **{interaction_video.component.label}***. By {interaction_video.author}",
                                 components=[])

        await ctx.send(".\n\n\n\n\n\n.")

bot.run(config.DISCORD_TOKEN)

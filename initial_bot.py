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
        # TODO Delete old Buttons
        rate_message = await ctx.send(message, components=[
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
        await rate_message.edit(components=[])
        await ctx.send(f"*Rated: **{interaction_rate.component.label}***. By {interaction_rate.author}")
        print(interaction_rate.component.label)

        # USE AS CLIP ####################################################################################
        # TODO Delete old Buttons
        clip_message = await ctx.send("Use as a **clip**?", components=[
            [Button(label="Yes", style=3, custom_id="yes"),
             Button(label="No", style=4, custom_id="no")]
        ])
        interaction_clip = await bot.wait_for("button_click")
        try:
            await interaction_clip.respond()
        except:
            pass
        # await ctx.send("***" + interaction_clip.component.label + f"***. By {interaction_clip.author}")
        print(interaction_clip.component.label)

        # Clip Title #####################################################################################
        if interaction_clip.component.label == "Yes":
            await clip_message.edit(f"*Use as Clip: **{interaction_clip.component.label}***. By {interaction_clip.author}",
                                    components=[])

            await ctx.send("Enter Clip Name:")
            while True:
                msg = await bot.wait_for("message")

                # TODO Delete old Buttons
                title_message = await ctx.send(f"Confirm? ({msg.content})", components=[
                    [Button(label="Yes", style=3, custom_id="yes"),
                     Button(label="No", style=4, custom_id="no")]
                ])

                interaction_title = await bot.wait_for("button_click")
                try:
                    await interaction_title.respond()
                except:
                    pass

                if interaction_title.component.label == "Yes":
                    await title_message.edit(f"Confirmed: ({msg.content})", components=[])
                    print(msg.content)
                    print(interaction_title.component.label)
                    break
                await title_message.delete()

        await ctx.send(".\n\n\n\n\n\n.")


    # clip_number = 4
    # print(clips["data"][clip_number])
    # await ctx.send("title\n" + clips["data"][clip_number]["thumbnail_url"].split("-preview")[0] + ".mp4")
    # await ctx.send(clips["data"][clip_number]["url"])

bot.run(config.DISCORD_TOKEN)

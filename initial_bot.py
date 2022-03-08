import discord
from discord.ext import commands

import config

bot = commands.Bot(command_prefix='!')


@bot.command()
async def status(ctx):
    await ctx.send('Pi Bot: ONLINE')


@bot.command()
async def chain(ctx):
    await ctx.send('!one')


@bot.command()  # DOESN'T WORK (not called by chain)
async def one(ctx):
    await ctx.send('!two')

bot.run(config.Token)

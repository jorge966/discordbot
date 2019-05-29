import discord
import botMain
import config
from discord.ext import commands
import time
import os

class OpenDota(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def runtime(self, ctx):
        """ Usage !runtime """
        current_time = (time.time() - botMain.Bot.start_time)/3600
        print('Bot has been running for: {0:.2f} hours'.format(current_time))
        await ctx.send('Bot has been running for: **{0:.2f}** hours'.format(current_time))

def setup(bot):
    openDota = OpenDota(bot)
    bot.add_cog(openDota)

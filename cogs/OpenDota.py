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
    async def getrecent(self, ctx):
        """ Usage !getrecent """
        pass

def setup(bot):
    openDota = OpenDota(bot)
    bot.add_cog(openDota)

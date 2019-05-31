import botMain
from discord.ext import commands
import time
import mongoDriver as md

guildDb = md.mongoConnection("127.0.0.1", "Channels", "JoinedChannels")

class Utilities(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def runtime(self, ctx):
        """ Usage !runtime """
        current_time = (time.time() - botMain.Bot.start_time)/3600
        print('Bot has been running for: {0:.2f} hours'.format(current_time))
        await ctx.send('Bot has been running for: **{0:.2f}** hours'.format(current_time))

    async def on_guild_join(self, guild):
        guild = {}
        guild['guild_id'] = guild.id
        guild['guild_name'] = guild.name
        guild['guild_owner_id'] = guild.owner_id
        guild['base_text_channel'] = guild.text_channels[0]
        guild['join_time'] = time.time()
        guildDb.insertOne(guild)

def setup(bot):
    util = Utilities(bot)
    bot.add_cog(util)

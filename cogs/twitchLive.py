from discord.ext import commands
import mongoDriver as md
from twitch import TwitchClient
import config

twitchDb = md.mongoConnection('127.0.0.1', 'TwitchInfo', 'Twitchusers')

class AddTwitch(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def live(self, ctx, arg):
        vars = twitchDb.getAllDocuments()
        twitch_name = None

        for item in vars:
            if arg == item['username']:
                twitch_name = item

        twitch_id = twitch_name['user_id']
        client = TwitchClient(config.twitch_client)
        channel = client.streams.get_stream_by_user(twitch_id)

        if channel == None:
            await ctx.send(twitch_name['username'] + " is not live right now")
        else:
            await  ctx.send(twitch_name['username'] + " is live right now!")
    @commands.command()
    async def addTwitchuser(self, ctx, username, user_id):
        user = username
        user_id = user_id

        Twitch_info = {}
        Twitch_info['username'] = user
        Twitch_info['user_id'] = int(user_id)

        twitchDb.insertOne(Twitch_info)

        await ctx.send("user has been added")

def setup(bot):
    addTwitch = AddTwitch(bot)
    bot.add_cog(addTwitch)
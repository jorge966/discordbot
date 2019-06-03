from discord.ext import commands
import mongoDriver as md
import json

acctIdDb = md.mongoConnection("127.0.0.1", "matchDatabase", "Users")
lastMatchDb = md.mongoConnection("127.0.0.1", "matchDatabase", "lastMatches")
servicesDb = md.mongoConnection("127.0.0.1", "OpenDota", "OpenDotaServices")

class AddDota(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def enableOpenDotaApi(self, ctx):
        empty_follows_account = {'accounts': []}
        empty_account_string = json.dumps(empty_follows_account)
        guild_obj = {}
        guild_obj['guild_id'] = ctx.guild.id
        guild_obj['followed_accounts'] = empty_account_string
        servicesDb.insertOne(guild_obj)

    @commands.command()
    async def test(self, ctx):
        steve_guild = self.bot.get_guild(584036142295285794)
        jorge_guild = self.bot.get_guild(547669771450187776)

    @commands.command()
    async def adduser(self, ctx, user, acct_id):

        acct_id = acct_id
        username = user
        vars_1 = acctIdDb.getAllDocuments()
        # First Load Existing Users
        for item in vars_1:
            if user == item['name']:
                await ctx.send("name is already in the system")
                break

            elif user != item["name"]:
                # Create the user data
                user = {}
                user['name'] = username
                user['account_id'] = int(acct_id)

                # Append the user to the userData file
                acctIdDb.insertOne(user)

                # Save the data

                await ctx.send("Successfully Added {}".format(username))
                break

    @commands.command()
    async def addMatchid(self, ctx, acct_id, match_id):

        acct_id = acct_id
        match_id = match_id

        lastMatch = {}
        lastMatch['account_id'] = acct_id
        lastMatch['match_id'] = int(match_id)

        lastMatchDb.insertOne(lastMatch)

        await  ctx.send("account id and match id saved")

    @commands.command()
    async def addMatchidDB(self, user, Match_id):
        username = user
        match = Match_id

        lastMatch = {}
        lastMatch['account_id'] = username
        lastMatch['match_id'] = int(match)

        lastMatchDb.insertOne(lastMatch)


def setup(bot):
    addDota = AddDota(bot)
    bot.add_cog(addDota)

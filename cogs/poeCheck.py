from discord.ext import commands,tasks
import mongoDriver as md
import requests
import json
import config
import time


#Work in progress
class CheckPoe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channelDb = md.mongoConnection("127.0.0.1", "Channels", "PoeChannels")
        self.pathDB = md.mongoConnection('127.0.0.1','Pathofexile','Pathdatabase')
        self.pathAccount = md.mongoConnection("127.0.0.1", 'Pathofexile', 'Account')
        self.lastActive = md.mongoConnection("127.0.0.1", 'Pathofexile', 'lastActive')

    @commands.command()
    async def addpoeCheck(self, ctx):
        attribute = {'guild_id': ctx.guild.id }
        update_attribute = {'active': 1}
        self.pathDB.updateByField(attribute, update_attribute)
        await ctx.send("You have successfully subscribed to the CheckPoe service")

    @commands.command()
    async def removepoeCheck(self, ctx):
        attribute = {'guild_id': ctx.guild.id}
        update_attribute = {'active': 0}
        self.pathDB.updateByField(attribute, update_attribute)
        await ctx.send("You have successfully unsubscribed to the CheckPoe service")

    @commands.command()
    async def addpoeAccount(self, ctx, account_name, name):
        filter = {'guild_id': ctx.guild.id}
        guild = self.pathDB.getOneDocumentByFilter(filter)
        if not guild['active'] or guild is None:
            await ctx.send("You cannot add an account if you are not subscribed to the CheckPoe service")
            await ctx.send("you can do !addpoeCheck to add yourself to the service")
        else:
            accountObject = {'account_name': account_name, 'name': name, 'active': 1}
            poeDb = self.return_guild_db()
            poeDb.upsertOneByField({'account_name': account_name}, accountObject)
            await ctx.send("Added {} to the poeCheck Service".format(name))

    @commands.command()
    async def removepoeAccount(self, ctx, name):
        filter = { 'guild_id': ctx.guild.id }
        guild = self.pathDB.getOneDocumentByFilter(filter)
        if not guild['active'] or guild is None:
            await ctx.send("You cannot remove an account if you are not subscribed to the OpenDota service")
            await ctx.send("you can do !addpoeCheck to add yourself to the service")
        else:
            attribute = { 'name': name}
            update_attribute = { 'active': 0 }
            poedDb = self.return_guild_db()
            poedDb.updateByField(attribute, update_attribute)
            await ctx.send("Removed {} to the poeCheck Service".format(name))


    @tasks.loop(seconds= 10)
    async def poeCheck(self):
        await self.bot.wait_until_ready()
        activeGuilds = self.get_active_guilds()

        for guild in activeGuilds:
            channel = self.bot.get_guild(guild['guild_id']).text_channel[0]
            activeAccounts = self.get_active_accounts() #returns all active accounts

            for account in activeAccounts:
                get_name = self.getlastActiveApi(account['account_name']) #checks the api with the account name
                lastactive = self.get_lastActiveDB() #checks the last active database



                for active in lastactive:
                    last_active = self.getlastActiveApi(get_name['name']) #api's current active name

                    if last_active == lastactive['name']:
                        await channel.send("{}'s last active character: {} is still alive in {}".format(account['name'], lastactive['name'], lastactive['class']))
                    elif not last_active == lastactive['name']:
                        checkpoe = self.getpoeChar(account['name'], last_active)
                        if checkpoe != 'Hardcore Legion':
                            await channel.send("{}'s last active character: {} is still alive in {}".format(account['name'], lastactive['name'], lastactive['class']))
                            time.sleep(2)
                            await channel.send("but it seems before this his last Character saved here {} died".format(lastactive['name']))
























    def getpoeChar(self, account_name , arg):
        poeDetails = self.getpoeApi(account_name)

        for character in poeDetails:
            if arg == character['name']:
                return character['league']



    def getpoeApi(self, account_name):
        url = 'https://www.pathofexile.com/character-window/get-characters?accountName=' + account_name
        return json.loads(requests.get(url).text)

    def getlastActiveApi(self, account_name):
        poeDetails = self.getpoeApi(account_name)

        for character in poeDetails:
            for key,value in character.items():
                if key == 'lastActive':
                    addActive = {'account_name': account_name, 'name': character['name']}
                    self.lastActive.insertOne(addActive)

                    return {
                        'name' : character['name'],
                        'league' : character['league'],
                        'class' : character['class'],
                        'level' : str(character['level'])
                    }

        return "Account Name not found"



    def get_active_guilds(self):
        filter = { 'active': 1 }
        return self.pathDB.getAllDocumentsByFilter(filter)

    def get_lastActiveDB(self):
        return self.lastActive.getAllDocuments()

    # Get all active accounts in guild
    def get_active_accounts(self):
        filter = { 'active': 1 }
        pathDb = self.return_guild_db()
        return pathDb.getAllDocumentsByFilter(filter)


    def return_guild_db(self):
        return md.mongoConnection("127.0.0.1", 'Pathofexile', 'Account')
    # below is the old code im trying to refactor and make into a task
    @commands.command()
    async def checkAccount(self, ctx, account_name):

        url = 'https://www.pathofexile.com/character-window/get-characters?accountName=' + account_name
        poe_web = requests.get(url)

        json_data = json.loads(poe_web.text)

        user_name = None
        ascendency = None
        level = None
        league = None
        for character in json_data:
            for key, value in character.items():
                if key == 'lastActive':
                    user_name = character['name']
                    league = character['league']
                    ascendency = character['class']
                    level = str(character['level'])

            print(type(user_name))
            print(type(level))
            print(type(ascendency))
            print(type(league))

            # if character['lastActive'] not in json_data:
            #     continue
            # elif character['league'] == 'Hardcore Legion' and character['lastActive'] == True:
            #     LastActive = character['lastActive']
            #     print(LastActive)
            #     user_name = character['name']
            #     ascendency = character['class']
            #     level = str(character['level'])
            #     league = character['league']

        if league == 'Hardcore Legion':
                await ctx.send('Your last played character is ' + user_name + ' level ' + level + ' as a ' + ascendency + ' in ' + league)
        else:
                await ctx.send('I dont see your last character in Hardcore legion so i think you died or havent played in the current league')
def setup(bot):
    checkaccount = CheckPoe(bot)
    bot.add_cog(checkaccount)





from discord.ext import commands,tasks
import mongoDriver as md
import requests
import json
import config
import time

#'name': 'spin_my_ass_fast', 'league': 'Hardcore Legion', 'classId': 4, 'ascendancyClass': 3, 'class': 'Champion', 'level': 86, 'experience': 1496324749, 'lastActive': True}


class CheckPoe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channelDb = md.mongoConnection("127.0.0.1", "Channels", "PoeChannels")
        self.pathDB = md.mongoConnection('127.0.0.1','Pathofexile','Pathdatabase')
        self.pathAccount = md.mongoConnection("127.0.0.1", 'Pathofexile', 'Account')
        self.lastActive = md.mongoConnection("127.0.0.1", 'Pathofexile', 'lastActive')
    @commands.command()
    async def poecheck(self, ctx):

        activeGuilds = self.get_active_guilds()

        for guild in activeGuilds:

            activeAccounts = self.get_active_accounts()  # returns all active accounts

            for account in activeAccounts:
                get_api_info = self.getlastActiveApi(account['account_name'])  # checks the api with the account name
                lastactive = self.get_lastActiveDB()  # checks the last active database

                for active in lastactive:
                    last_active = self.getlastActiveApi(get_api_info['name'])  # api's current active name

                    if last_active == active['name']:
                        ctx.send("{}'s last active character: {} is still alive in {}".format(account['name'],last_active['name'],get_api_info['class']))
                    elif not last_active == active['name']:
                        checkpoe = self.getpoeChar(account['name'], last_active)
                        if checkpoe != 'Hardcore Legion':
                                ctx.send("{}'s last active character: {} is still alive in {}".format(account['name'],lastactive['name'],get_api_info['class']))
                                time.sleep(2)
                                ctx.send("but it seems before this his last Character saved here {} died".format(lastactive['name']))


    def getpoeChar(self, account_name, arg):
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
            for key, value in character.items():
                if key == 'lastActive':
                    addActive = {'account_name': account_name, 'name': character['name']}
                    self.lastActive.insertOne(addActive)

                    return {
                        'name': character['name'],
                        'league': character['league'],
                        'class': character['class'],
                        'level': character['level']
                    }

        return "Account Name not found"


    def get_active_guilds(self):
        filter = {'active': 1}
        return self.pathDB.getAllDocumentsByFilter(filter)


    def get_lastActiveDB(self):
        return self.lastActive.getAllDocuments()


    # Get all active accounts in guild
    def get_active_accounts(self):
        filter = {'active': 1}
        pathDb = self.return_guild_db()
        return pathDb.getAllDocumentsByFilter(filter)


    def return_guild_db(self):
        return md.mongoConnection("127.0.0.1", 'Pathofexile', 'Account')
def setup(bot):
    checkaccount = CheckPoe(bot)
    bot.add_cog(checkaccount)
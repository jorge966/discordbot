from discord.ext import commands,tasks
import mongoDriver as md
import requests
import json
import config
import time
import pprint

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
                get_api_info = self.getlastActiveApi(account['account_name'])# checks the api with the account name
                lastactive = self.get_lastActiveDB()  # checks the last active database




                for active in lastactive:
                    #print(active)

                    last_active = get_api_info['name']#self.getlastActiveApi(account['account_name'])  # api's current active name
                    #self.getlastActiveApi(This_Is_My_New_ED_rip)


                    if last_active == active['name']:
                        await ctx.send("{}'s has no recent death's in Hardcore Legion".format(account['name']))


                    elif not last_active == active['name']:
                        checkpoe = self.getpoeChar(account['account_name'], last_active)
                        if checkpoe != 'Hardcore Legion':
                                await ctx.send("{}'s character: {}, has Died since the last time you checked".format(account['name'],lastactive['name']))





    def getpoeChar(self, account_name, arg):
        poeDetails = self.getpoeApi(account_name)


        for character in poeDetails:
            if arg == character['name']:
                return character['league']


    def getpoeApi(self, account_name):
        url = 'https://www.pathofexile.com/character-window/get-characters?accountName=' + account_name
        return json.loads(requests.get(url).text)

    #fixing this so it saves all the name's so it just reads the db and matches with api to see who has died or not
    def getlastActiveApi(self, account_name):
        poeDetails = self.getpoeApi(account_name)
        #pprint.pprint(poeDetails)
        check_accounts = self.get_active_accounts()
        get_lastactiveDB = self.get_lastActiveDB()

        for character in poeDetails: #check poe api character# #searches the api for a specific char that has a key of "last Active"
             if character['league'] == 'Hardcore Legion':
                print(character)
                is_in_list = False
                for item in check_accounts:# check the account database for current accounts that are active
                    for char_info in get_lastactiveDB:
                        print(account_name)
                        print(item['account_name'])
                        print(character['name'])
                        print(char_info['name'])
                        if account_name.upper() == item['account_name'].upper() and character['name'].upper() == char_info['name'].upper():
                            is_in_list = True

                print(is_in_list)

                if is_in_list == True:
                    return  {
                        'name': character['name'],
                        'league': character['league'],
                        'class': character['class'],
                        'level': character['level']
                    }
                else:
                    addActive = {'account_name': account_name, 'name': character['name'],'league': character['league']}
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
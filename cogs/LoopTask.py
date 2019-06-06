from discord.ext import tasks,commands
import requests
import json
import time
import mongoDriver as md

class TaskDota(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channelDb = md.mongoConnection("127.0.0.1", "Channels", "JoinedChannels")
        self.openDotaDb = md.mongoConnection("127.0.0.1", "OpenDota", "OpenDotaServices")
        self.open_dota_task.start()

    #<editor-fold> OpenDota Discord Commands

    # Add a guild to the OpenDota service
    @commands.command()
    async def addopendota(self, ctx):
        attribute = { 'guild_id': ctx.guild.id }
        update_attribute = { 'active': 1 }
        self.openDotaDb.updateByField(attribute, update_attribute)
        await ctx.send("You have successfully subscribed to the OpenDota service")

    # Remove a guild from the OpenDota service
    @commands.command()
    async def removeopendota(self, ctx):
        attribute = { 'guild_id': ctx.guild.id }
        update_attribute = { 'active': 0 }
        self.openDotaDb.updateByField(attribute, update_attribute)
        await ctx.send("You have successfully unsubscribed to the OpenDota service")

    # Add an account to the OpenDota service
    @commands.command()
    async def addaccount(self, ctx, account_id, nickname):
        filter = { 'guild_id': ctx.guild.id }
        guild = self.openDotaDb.getOneDocumentByFilter(filter)
        if not guild['active']:
            await ctx.send("You cannot add an account if you are not subscribed to the OpenDota service")
        else:
            accountObject = { 'account_id': account_id, 'nickname': nickname, 'last_match_id': 0, 'active': 1 }
            guildDb = self.return_guild_db(ctx.guild.id)
            guildDb.upsertOneByField({'account_id': account_id}, accountObject)
            await ctx.send("Added {} to the OpenDota Service".format(nickname))

    # Remove an account from the OpenDota service
    @commands.command()
    async def removeaccount(self, ctx, account_id):
        filter = { 'guild_id': ctx.guild.id }
        guild = self.openDotaDb.getOneDocumentByFilter(filter)
        if not guild['active']:
            await ctx.send("You cannot remove an account if you are not subscribed to the OpenDota service")
        else:
            attribute = { 'account_id': account_id }
            update_attribute = { 'active': 0 }
            guildDb.updateByField(attribute, update_attribute)
            await ctx.send("Removed {} to the OpenDota Service".format(account_id))

    #</editor-fold>

    #<editor-fold> OpenDota Background Loop

    # Defines the Loop that will run on Bot Start
    @tasks.loop(seconds=10.0)
    async def open_dota_task(self):
        await self.bot.wait_until_ready()
        activeGuilds = self.get_active_guilds()

        for guild in activeGuilds:
            channel = self.bot.get_guild(guild['guild_id']).text_channels[0]
            activeAccounts = self.get_active_accounts(guild)

            for account in activeAccounts:

                db_match_id = str(self.get_last_match(account['account_id'], guild['guild_id']))
                opendota_match_id = str(self.opendota_recent_matches(account['account_id']))

                if not db_match_id == opendota_match_id:
                    matchData = self.match_information(opendota_match_id, account['account_id'])

                    win_msg = "{} won their recent match as {}".format(matchData['username'], matchData['hero_name'])
                    loss_msg = "{} lost their recent match as {}".format(matchData['username'], matchData['hero_name'])
                    if (matchData['is_radiant'] and matchData['radiant_win']) or (not matchData['is_radiant'] and not matchData['radiant_win']):
                        await channel.send(win_msg)
                    else:
                        await channel.send(loss_msg)

                    guildDb = self.return_guild_db(guild['guild_id'])
                    filter = { 'account_id': account['account_id'] }
                    field = { 'last_match_id': opendota_match_id }
                    guildDb.updateByField(filter, field)

    #</editor-fold>

    #<editor-fold> Api Functions

    # Returns the most recent match ID given account ID from opendota
    def opendota_recent_matches(self, account_id):
        url = "https://api.opendota.com/api/players/{}/recentMatches".format(account_id)
        json_data = json.loads(requests.get(url).text)
        return json_data[0]['match_id']

    # Returns the hero name given hero ID from opendota
    def opendota_hero_name(self, hero_id):
        json_data = json.loads(requests.get("https://api.opendota.com/api/heroes").text)
        for item in json_data:
            if str(hero_id) == str(item["id"]):
                return item["localized_name"]
        return "Hero ID not found"

    # Returns a JSON object with the specified match ID from opendota
    def opendota_get_match(self, match_id):
        url = "https://api.opendota.com/api/matches/{}".format(match_id)
        return json.loads(requests.get(url).text)

    #</editor-fold>

    #<editor-fold> Helper Functions

    # Get match information given match ID
    def match_information(self, match_id, account_id):
        matchDetails = self.opendota_get_match(match_id)
        players = matchDetails["players"]
        for player in players:
            if str(account_id) == str(player['account_id']):
                return {
                    'account_id': account_id,
                    'username': player['personaname'],
                    'is_radiant': player['isRadiant'],
                    'radiant_win': player['radiant_win'],
                    'hero_name': self.opendota_hero_name(player['hero_id'])
                }
        return "Account ID not found in this Match"

    # Get all active guilds
    def get_active_guilds(self):
        filter = { 'active': 1 }
        return self.openDotaDb.getAllDocumentsByFilter(filter)

    # Get all active accounts in guild
    def get_active_accounts(self, guild):
        filter = { 'active': 1 }
        guildDb = self.return_guild_db(guild['guild_id'])
        return guildDb.getAllDocumentsByFilter(filter)

    # Get last match_id for specified account id
    def get_last_match(self, account_id, guild_id):
        filter = { 'account_id': account_id }
        guildDb = self.return_guild_db(guild_id)
        obj = guildDb.getOneDocumentByFilter(filter)
        return obj['last_match_id']

    # Return a mongo connection object with specified guild_id
    def return_guild_db(self, guild_id):
        return md.mongoConnection("127.0.0.1", "OpenDotaGuildDatabases", str(guild_id))

    #</editor-fold>

def setup(bot):
    taskdota = TaskDota(bot)
    bot.add_cog(taskdota)

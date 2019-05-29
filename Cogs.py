from discord.ext import commands
import json
import requests
import time as time
import mongoDriver as md
import config
from twitch import TwitchClient


bot = commands.Bot(command_prefix='!')
acctIdDb = md.mongoConnection("127.0.0.1", "matchDatabase", "Users")
lastMatchDb = md.mongoConnection("127.0.0.1", "matchDatabase", "lastMatches")
twitchDb = md.mongoConnection('127.0.0.1', 'TwitchInfo', 'Twitchusers')

class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def gr(self, ctx, arg):
        isAccountId = False
        try:
            input = int(arg)
            isAccountId = True
        except:
            pass

        if isAccountId:
            recent = requests.get("https://api.opendota.com/api/players/" + str(arg) + "/recentMatches")
            await ctx.send("getting recent matches...")
            time.sleep(2)
            json_data = json.loads(recent.text)
            match_id = json_data[0]['match_id']
            url = "https://api.opendota.com/api/matches/" + str(match_id)
            await ctx.send("getting match...")
            time.sleep(2)
            data = requests.get(url)
            json_data2 = json.loads(data.text)
            players = json_data2["players"]
            temp = None
            temp_hero = None

            for item in players:
                if int(arg) == item["account_id"]:
                    temp = item
            persona_name = temp["personaname"]
            radiant_win = temp["radiant_win"]
            is_radiant = temp["isRadiant"]
            hero_id = temp["hero_id"]

            get_hero = requests.get("https://api.opendota.com/api/heroes")
            load_hero = json.loads(get_hero.text)

            for item in load_hero:
                if hero_id == item["id"]:
                    temp_hero = item["localized_name"]

            if radiant_win:
                if is_radiant:
                    await ctx.send(persona_name + " won their last game" + " as " + temp_hero)
                else:
                    await ctx.send(persona_name + " lost their last game" + " as " + temp_hero)
            elif not radiant_win:
                if not is_radiant:
                    await ctx.send(persona_name + " won their last game" + " as " + temp_hero)
                else:
                    await ctx.send(persona_name + " lost their last game" + " as " + temp_hero)

        elif not isAccountId:
            # Load User Data

            vars_name = acctIdDb.getAllDocuments()
            # Found User Bool
            userFound = False

            # User Variable
            foundUser = None

            # Loop through users
            for item in vars_name:
                if arg == item["name"]:
                    foundUser = item
                    userFound = True
                    break

            user_id = foundUser["account_id"]
            url = "https://api.opendota.com/api/players/" + str(user_id) + "/recentMatches"
            # print(url)
            recent = requests.get(url)
            await ctx.send("getting recent matches...")
            time.sleep(2)
            json_data = json.loads(recent.text)
            match_id = json_data[0]['match_id']
            url = "https://api.opendota.com/api/matches/" + str(match_id)
            await ctx.send("getting match...")
            time.sleep(2)
            data = requests.get(url)
            json_data2 = json.loads(data.text)
            players = json_data2["players"]
            temp = None
            temp_hero = None

            for item in players:
                if user_id == item["account_id"]:
                    temp = item
            persona_name = temp["personaname"]
            radiant_win = temp["radiant_win"]
            is_radiant = temp["isRadiant"]
            hero_id = temp["hero_id"]

            get_hero = requests.get("https://api.opendota.com/api/heroes")
            load_hero = json.loads(get_hero.text)

            for item in load_hero:
                if hero_id == item["id"]:
                    temp_hero = item["localized_name"]

            if radiant_win:
                if is_radiant:
                    await ctx.send(persona_name + " won their last game" + " as " + temp_hero)
                else:
                    await ctx.send(persona_name + " lost their last game" + " as " + temp_hero)
            elif not radiant_win:
                if not is_radiant:
                    await ctx.send(persona_name + " won their last game" + " as " + temp_hero)
                else:
                    await ctx.send(persona_name + " lost their last game" + " as " + temp_hero)
        else:
            await  ctx.send("I couldn't find anything in the database")

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
    def addMatchidDB(self, user, Match_id):
        username = user
        match = Match_id

        lastMatch = {}
        lastMatch['account_id'] = username
        lastMatch['match_id'] = int(match)

        lastMatchDb.insertOne(lastMatch)

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
    async def addTwitchuser(self, ctx, username, user_id):
        user = username
        user_id = user_id

        Twitch_info = {}
        Twitch_info['username'] = user
        Twitch_info['user_id'] = int(user_id)

        twitchDb.insertOne(Twitch_info)

        await ctx.send("user has been added")

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

def setup(bot):
    bot.add_cog(MainCog(bot))


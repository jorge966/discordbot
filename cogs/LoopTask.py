from discord.ext import tasks,commands
import requests
import json
import mongoDriver as md


acctIdDb = md.mongoConnection("127.0.0.1", "matchDatabase", "Users")
lastMatchDb = md.mongoConnection("127.0.0.1", "matchDatabase", "lastMatches")

class TaskDota(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.slow_count.start()

    @tasks.loop(seconds=10.0)
    async def slow_count(self):
        steve_channel = self.bot.get_guild(584036142295285794).text_channels[0]
        jorge_channel = self.bot.get_guild(547669771450187776).text_channels[0]


        vars_user = acctIdDb.getAllDocuments()
        vars_match = lastMatchDb.getAllDocuments()

        # Found User Bool
        userFound = False

        # User Variable
        foundUser = None
        # Loop through users
        for user in vars_user:
            for match in vars_match:
                if match['account_id'] == str(user["account_id"]):
                    foundUser = user
                    userFound = True
                    break
        #need to rewind mongo cursor after every use
        vars_match.rewind()
        vars_user.rewind()

        user_id = foundUser["account_id"]

        url = "https://api.opendota.com/api/players/" + str(user_id) + "/recentMatches"
        #print(url)
        recent = requests.get(url)
        #print("getting recent matches...")
        json_data = json.loads(recent.text)
        updated_match_id = json_data[0]['match_id']
        newMatch = None
        foundmatch = False
        oldMatch = None
        for item in vars_match:
            oldMatch = item['match_id']
            break
        vars_match.rewind()

        for item in vars_match:
            if updated_match_id != item['match_id']:
                item['match_id'] = updated_match_id
                foundmatch = True
                newMatch = item
                lastMatchDb.updateOneByMatchid(oldMatch, newMatch['match_id'])
                print("updated")
                url = "https://api.opendota.com/api/matches/" + str(newMatch['match_id'])
                print("getting match...")
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
                        jorge_channel.send(persona_name + " won their last game" + " as " + temp_hero)
                        print(persona_name + " won their last game" + " as " + temp_hero)
                    else:
                        jorge_channel.send(persona_name + " lost their last game" + " as " + temp_hero)
                        print(persona_name + " lost their last game" + " as " + temp_hero)
                elif not radiant_win:
                    if not is_radiant:
                        jorge_channel.send(persona_name + " won their last game" + " as " + temp_hero)
                        print(persona_name + " won their last game" + " as " + temp_hero)
                    else:
                        jorge_channel.send(persona_name + " lost their last game" + " as " + temp_hero)
                        print(persona_name + " lost their last game" + " as " + temp_hero)
                break
            else:
                print("check")
                break
        vars_match.rewind()
        vars_user.rewind()

def setup(bot):
    taskdota = TaskDota(bot)
    bot.add_cog(taskdota)

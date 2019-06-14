from discord.ext import commands
import mongoDriver as md
import requests
import json
import config

#'name': 'spin_my_ass_fast', 'league': 'Hardcore Legion', 'classId': 4, 'ascendancyClass': 3, 'class': 'Champion', 'level': 86, 'experience': 1496324749, 'lastActive': True}
#pathDB = md.mongoConnection('127.0.0.1','Pathofexile','Account')

class CheckPoe(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

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






















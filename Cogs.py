from discord.ext import commands
import json
import requests



class MainCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    @commands.command()
    async def gr(ctx, arg):
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

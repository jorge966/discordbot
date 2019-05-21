from discord import Client

import config
import requests
import json
from discord.ext import commands, tasks
import time as time
import mongoDriver as md
import pprint as pp

acctIdDb = md.mongoConnection("127.0.0.1", "matchDatabase", "Users")
lastMatchDb = md.mongoConnection("127.0.0.1", "matchDatabase", "lastMatches")





bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
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
        #print(url)
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

@bot.command()
async def adduser(ctx, user, acct_id):

    acct_id = acct_id
    username = user

    # First Load Existing Users


    # Create the user data
    user = {}
    user['name'] = username
    user['account_id'] = int(acct_id)

    # Append the user to the userData file
    acctIdDb.insertOne(user)

    # Save the data


    await ctx.send("Successfully Added {}".format(username))


@bot.command()
async def addMatchid(ctx, acct_id , match_id):

    acct_id = acct_id
    match_id = match_id

    lastMatch = {}
    lastMatch['account_id'] = acct_id
    lastMatch['match_id'] = int(match_id)

    lastMatchDb.insertOne(lastMatch)

    await  ctx.send("account id and match id saved")


def addMatchidDB(user , Match_id):
    username = user
    match = Match_id



    lastMatch = {}
    lastMatch['account_id'] = username
    lastMatch['match_id'] = int(match)

    lastMatchDb.insertOne(lastMatch)

@tasks.loop(seconds=10.0)
async def slow_count():
    
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
    for item in vars_match:
        if updated_match_id != item['match_id']:
            item['match_id'] = updated_match_id
            foundmatch = True
            newMatch = item
            print(newMatch)
            lastMatchDb.updateOneByAccountId(user_id, newMatch)
            print("updated")
            url = "https://api.opendota.com/api/matches/" + str(newMatch)
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
                    print(persona_name + " won their last game" + " as " + temp_hero)
                else:
                    print(persona_name + " lost their last game" + " as " + temp_hero)
            elif not radiant_win:
                if not is_radiant:
                    print(persona_name + " won their last game" + " as " + temp_hero)
                else:
                    print(persona_name + " lost their last game" + " as " + temp_hero)
            break
        else:
            await channel.send("no new update")
            break

    #need to rewind mongo cursor after every use
    vars_match.rewind()
    vars_user.rewind()

slow_count.start()

bot.run(config.Bot_Token)
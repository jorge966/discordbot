import config
import requests
import json
from discord.ext import commands , tasks
import time as time



bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def hi(ctx):
    await ctx.send('Hello')

@bot.command()
async def wins(ctx, input):
    isAccountId = False
    try:
        input = int(input)
        isAccountId = True
    except:
        pass

    if isAccountId:
        winloss = requests.get("https://api.opendota.com/api/players/" + str(input) + "/wl")
        await ctx.send(winloss.text)

    if not isAccountId:
        user_Data = loadUsers()
        userFound = False
        temp = None
        for item in user_Data["users"]:
            if input == item["name"]:
                temp = item
                userFound = True
                break
        account_id_get = temp["account_id"]

        winloss = requests.get("https://api.opendota.com/api/players/" + str(account_id_get) + "/wl")
        await ctx.send(winloss.text)

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
        userData = loadUsers()

        # Found User Bool
        userFound = False

        # User Variable
        foundUser = None

        # Loop through users
        for item in userData['users']:
            if arg == item["name"]:
                foundUser = item
                userFound = True
                break

        user_id = foundUser["account_id"]
        url = "https://api.opendota.com/api/players/" + str(user_id) + "/recentMatches"
        print(url)
        recent = requests.get(url)
        await ctx.send("getting recent matches...")
        time.sleep(2)
        json_data = json.loads(recent.text)
        match_id = json_data[0]['match_id']
        url = "https://api.opendota.com/api/matches/" + str(match_id)
        addMatchid(arg, match_id)
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


#@bot.command()
#async def gr2(ctx, input):

@bot.command()
async def adduser(ctx, user, acct_id):

    acct_id = acct_id
    username = user

    # First Load Existing Users
    userData = loadUsers()

    # Create the user data
    user = {}
    user['name'] = username
    user['account_id'] = int(acct_id)

    # Append the user to the userData file
    userData['users'].append(user)

    # Save the data
    saveUsers(userData)

    await ctx.send("Successfully Added {}".format(username))

def addMatchid(user , Match_id):
    username = user
    match = Match_id

    matchData = loadMatchid()

    lastMatch = {}
    lastMatch['name'] = username
    lastMatch['match_id'] = int(match)

    matchData['Matches'].append(lastMatch)

    saveMatchid(matchData)



@bot.command()
async def findUserByName(ctx, name):
    # Load userData
    userData = loadUsers()

    # Found User Bool
    userFound = False

    # User Variable
    foundUser = None

    # Loop through users
    for item in userData['users']:
        if item['name'] == name:
            foundUser = item
            userFound = True
            break

    if userFound:
        await ctx.send("User Found. Name: {}, Account Id: {}".format(foundUser['name'], foundUser['account_id']))
    else:
        await ctx.send("User Not Found")

# Helper Functions
def saveUsers(json_file):
    with open('magic.txt', 'w') as outfile:
        json.dump(json_file, outfile)


def saveMatchid(json_file):
    with open('matchid.txt', 'w') as outfile:
        json.dump(json_file, outfile)

def loadUsers():
    temp = None
    with open('magic.txt') as json_file:
        data = json.load(json_file)
        temp = data
    return temp

def loadMatchid():
    temp = None
    with open('matchid.txt') as json_file:
        data = json.load(json_file)
        temp = data
    return temp

@tasks.loop(seconds=5.0)
async def slow_count():
    print("ping")




slow_count.start()


bot.run(config.Bot_Token)
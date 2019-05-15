import config
import requests
import json
from discord.ext import commands
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
async def wins(ctx):
    winloss = requests.get("https://api.opendota.com/api/players/92576390/wl")
    await ctx.send(winloss.text)

@bot.command()
async def gr(ctx, arg):
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

bot.run(config.Bot_Token)
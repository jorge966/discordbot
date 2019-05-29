import discord
import config
from discord.ext import commands
import time
import sched
import asyncio

class Bot(commands.Bot):

    start_time = time.time()

    def __init__(self, command_prefix, description=None, pm_help=False, **options):
        super().__init__(command_prefix, description, pm_help, **options)
        self.initial_config()
        self.initial_extensions()
        self.initial_listener()

    def initial_config(self):
        self.token = config.Bot_Token
        self.username = config.Bot_username
        self.app_id = config.App_ID
        self.app_secret = config.App_Secret

    def initial_extensions(self):
        self.load_extension('Utilities')
        self.load_extension('OpenDota')

    def initial_listener(self):
        self.add_listener(self.startup_message, 'on_ready')

    async def startup_message(self):
        print("Logged in as {}".format(self.username))
        print("Bot ID: {}".format(self.app_id))
        print("-----------")
        self.start_time = time.time()

import discord
import config
from discord.ext import commands
import time
import sched

class Bot(commands.Bot):

    start_time = time.time()

    def __init__(self, command_prefix, formatter=None,description=None, **options):
        super().__init__(command_prefix, formatter, description , **options)

    def initial_config(self):
        self.token = config.Bot_Token
        self.username = config.Bot_username
        self.app_id = config.App_ID
        self.app_secret = config.App_Secret

    def initial_extensions(self):
        def load_extension(name):
            self.load_extension('Cogs.{0}'.format(name))
        load_extension('MainCog')


    def initial_listener(self):
        self.add_listener(self.startup_message, 'on_ready')
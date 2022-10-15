from .commands import CommandsCog
from . import config

import discord

bot = discord.Bot(
    debug_guilds=[810742455745773579],
    intents=discord.Intents(guilds=True, members=True)
)
bot.add_cog(CommandsCog())

from .automated import *
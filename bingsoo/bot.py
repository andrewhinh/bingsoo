from .commands import CommandsCog

import discord

bot = discord.Bot(
    debug_guilds=[810742455745773579],
    intents=discord.Intents(guilds=True)
)
bot.add_cog(CommandsCog())

from .bot import bot

@bot.event
async def on_ready():
    print('Bot is running!')
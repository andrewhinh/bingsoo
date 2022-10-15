from .bot import bot
import os
from dotenv import load_dotenv

load_dotenv(override=True)

bot.run(os.environ["BOT_TOKEN"])


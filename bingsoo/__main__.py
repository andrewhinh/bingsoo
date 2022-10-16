from .bot import bot
from dotenv import load_dotenv
import os

load_dotenv(override=True)

bot.run(os.environ["BOT_TOKEN"], )


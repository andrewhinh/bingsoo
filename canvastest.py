# Import the Canvas class
from canvasapi import Canvas
import requests
from markdownify import markdownify as md
from discord import Bot
from pprint import pprint

import discord
import functools

import base64
bot = Bot(intents=discord.Intents(guilds=True))
# bot = Bot(intents=discord.Intents(guilds=True, members=True))

discord_md = functools.partial(md, convert=['b', 'i', 'blockquote', 'code', 'a', 's', ''])
md(convert=[''])
discord_md()

@bot.event
async def on_ready():
    # Canvas API URL
    API_URL = "https://ucmerced.instructure.com/"
    # Canvas API key
    API_KEY = "1101~DZsUqsZ9lEJx1YuHHg1VF1jCX8d0FSznxrMAO4OvHqOdFejPjEPnMjA2HTsY6Shl"

    # Initialize a new Canvas object
    canvas = Canvas(API_URL, API_KEY)
    courses = canvas.get_courses(enrollment_state="active")
    # announcements = canvas.get_announcements([*courses])
    announcements = canvas.get_announcements(list(courses))
    # print(bot.guilds)
    guild = bot.get_guild(810742455745773579)
    # print(announcements)
    for ann in announcements:
        # print(md(ann.message))
        await bot.get_guild(810742455745773579).get_channel(945195805688594502).send(md(ann.message))




# print(courses)
# group = Group()
# groups = canvas.get_groups()
# print(groups)
# pprint(canvas.get_announcements(context_codes = courses))
# for course in courses:
#     print(type(course))
#     print(canvas.get_announcements(course))
    # pprint(course.get_gradebook_history_dates)
    # print()

# get_settings

# bot.run('NzIyOTYxNDU2MzExNjk3NTEw.XuxSKA._-Jf3n9mos1H7p5r-4uptubJcqs')

bot.run(base64.b64decode(b'T0RFNE5qZ3pOak0zT1RNMU16YzBNelUyLllFYm9qUS40ZkY4d3VVRDduaE1KVU5QSFVjN1kwTFFhUlU=').decode())
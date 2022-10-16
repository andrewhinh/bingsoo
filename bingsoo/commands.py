from discord.ext import commands
from discord.commands import Option
from canvasapi import Canvas
from dotenv import load_dotenv
import os

load_dotenv(override=True)

from datetime import datetime
import asyncio
import discord
from .utils import *

class CommandsCog(commands.Cog):
    get_commands = discord.SlashCommandGroup(
        'get',
        "Commands used to get various information about the bot."
    )
    choose_commands = discord.SlashCommandGroup(
        'choose',
        "Commands used to get various information about the bot."
    )

    @get_commands.command(
        name='courses',
        description='Use this to see the courses I think you are enrolled in.'
    )
    async def get_courses(self, ctx: discord.ApplicationContext):
        # Canvas API URL
        API_URL = "https://ucmerced.instructure.com/"
        # Canvas API key
        API_KEY = os.environ['CANVAS_API_KEY']
        # TODO: fetch API creds based on who used it!
        canvas = Canvas(API_URL, API_KEY)
        courses = canvas.get_courses(enrollment_state='active')
        
        await ctx.respond(f"**Courses**:\n{chr(10).join(map(str, courses))}")

    @get_commands.command(
        name='assignment',
        description='Use this to see any assignments upcoming.'
    )
    async def get_assignments(self, ctx: discord.ApplicationContext):
        # Canvas API URL
        API_URL = "https://ucmerced.instructure.com/"
        # Canvas API key
        API_KEY = os.environ['CANVAS_API_KEY']
        # TODO: fetch API creds based on who used it!
        canvas = Canvas(API_URL, API_KEY)
        courses = canvas.get_courses(enrollment_state='active')

        # await ctx.respond("dfsd")
        # await ctx.respond(f"**Assignments**:\n{chr(10).join(map(lambda course: f"{course!s} {chr(10).join(map(str, course.get_assigment()))}", courses))}")
        assignments = []
        assignment_dict = {}

        counter = 0
        for course in courses:
            # assignment_str += f"__{course!s}__"
            print(course)
            assignment_dict[course.name] = {}
            for assignment in course.get_assignments():
                try:
                    assdate = datetime.fromisoformat(assignment.due_at[0:-1])
                except TypeError as e:
                    pass
                if assdate >= datetime.now():
                    counter+=1
                    temp_dict = {}
                    temp_dict['course'] = course.name
                    temp_dict['assignment_name'] = assignment.name
                    temp_dict['assignment_date'] = assdate
                    assignment_dict[course.name] = temp_dict
            if counter == 0:
                assignment_dict.pop(course.name, None)
            counter = 0

            print(assignment_dict)
            # print(assignment_str)
        await ctx.send("fdsfd")

    @choose_commands.command()
    async def classes(self, ctx):
        API_URL = "https://ucmerced.instructure.com/"
        # Canvas API key
        PI_KEY = os.environ['CANVAS_API_KEY']
        # TODO: fetch API creds based on who used it!
        canvas = Canvas(API_URL, API_KEY)
        # courses = canvas.get_courses(enrollment_state='active')
        # map(str, canvas.get_courses(enrollment_state='active'))
        choose_classes = ChooseClasses(list(map(str, canvas.get_courses(enrollment_state='active'))))
        ready = asyncio.Event()
        # @discord.ui.button(label="Submit", style=discord.ButtonStyle.success, emoji="✔")
        @discord.ui.button(label="Submit", style=discord.ButtonStyle.success, row=1)
        async def submit_button(view, button, interaction):
            view.disable_all_items()
            await interaction.message.edit(content="Choose the classes you want announced", view=view)
            await interaction.response.send_message("Classes saved!")
            ready.set()
        await ctx.respond("Choose the classes you want announced", view=ViewWithItemCallbackType(choose_classes, item_callback_type=[submit_button]))
        await ready.wait()
        await ctx.respond('after button is pressed :)')
        # Do stuff after the button is pressed
        # await ctx.interaction.edit_original_message(
        #     ctx.respond("")
        # )
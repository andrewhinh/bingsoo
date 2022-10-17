from discord.ext import commands
from discord.commands import Option
from canvasapi import Canvas
from dotenv import load_dotenv
import os
from .chatbot.context_type import FindType
# from chatbot.context_type import FindType
from .chatbot.utils.get_context import getSyllabuses, getAssignments
from .chatbot.chatbot import Answer


load_dotenv(override=True)

from datetime import datetime
import asyncio
import discord
from .utils import ChooseClasses, ChooseAssignments, convert_to_item

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
        assignment_dict = {}

        choice_courses = canvas.get_courses(enrollment_state='active')
        choose_classes = ChooseAssignments(list(map(str, choice_courses)))
        choose_classes._selected_values = list(map(str, choice_courses))
        ready = asyncio.Event()
        view = discord.ui.View(choose_classes)
        @convert_to_item
        @discord.ui.button(label="Submit", style=discord.ButtonStyle.success, row=1)
        async def submit_button(button, interaction):
            view.disable_all_items()
            await interaction.message.edit(content="Choose which classes to show assignments from", view=view)
            ready.set()
        view.add_item(submit_button)
        await ctx.respond("Choose which classes to show assignments from", view=view)
        await ready.wait()
        print(choose_classes.values)
        # for course in choice_courses:
        #     print(course.name)
        string_assignment = ""
        for course in choice_courses:
            # print(course.name)
            for i in range(len(choose_classes.values)):
                if course.name in choose_classes.values[i]:
                    # await ctx.respond(course.)
                    for assignment in course.get_assignments():
                        try:
                            assdate = datetime.fromisoformat(assignment.due_at[0:-1])
                        except TypeError as e:
                            pass
                        if assdate >= datetime.now():
                            string_assignment += f"{assignment.name} due at {str(assdate)}\n"
                            # await ctx.respond(assignment.name + " due at " + str(assdate))
            # if course.name in choose_classes.values:
            #     print(course)

        await ctx.respond(string_assignment)
        # await ctx.respond('after button is pressed :)')

    @choose_commands.command()
    async def classes(self, ctx):
        API_URL = "https://ucmerced.instructure.com/"
        # Canvas API key
        API_KEY = os.environ['CANVAS_API_KEY']
        # TODO: fetch API creds based on who used it!
        canvas = Canvas(API_URL, API_KEY)
        # courses = canvas.get_courses(enrollment_state='active')
        # map(str, canvas.get_courses(enrollment_state='active'))
        choose_classes = ChooseClasses(list(map(str, canvas.get_courses(enrollment_state='active'))))
        ready = asyncio.Event()
        # @discord.ui.button(label="Submit", style=discord.ButtonStyle.success, emoji="✔")
        view = discord.ui.View(choose_classes)
        @convert_to_item
        @discord.ui.button(label="Submit", style=discord.ButtonStyle.success, row=1)
        async def submit_button(button, interaction):
            view.disable_all_items()
            await interaction.message.edit(content="Choose the classes you want announced", view=view)
            await interaction.response.send_message("Classes saved!")
            ready.set()
        view.add_item(submit_button)
        await ctx.respond("Choose the classes you want announced", view=view)
        await ready.wait()
        # await ctx.respond('after button is pressed :)')
        # Do stuff after the button is pressed
        # await ctx.interaction.edit_original_message(
        #     ctx.respond("")
        # )
    
    @commands.slash_command(
        description="Ask me a question about your homework!",
        options=[
            Option(
                str,
                name='question',
                description='Type your question here.'
            )
        ]
    )
    async def ask(self, ctx: discord.ApplicationContext, question: str):
        # ready = asyncio.Event()
        CONTEXT_TYPE = FindType().predict(question)
        CONTEXT = getAssignments() #getSyllabuses() if CONTEXT_TYPE=="syllabus" else getAssignments()
        ANSWER = Answer().predict(question, CONTEXT, CONTEXT_TYPE)
        print(ANSWER)
        await ctx.send(ANSWER)
        # await ready.wait()
        # await ctx.respond(f'This again? The exam is on Wednesday, 10/12/2022 from 1:30 pm - 2:45 am in COB2-140. Please take note of this in the future.')
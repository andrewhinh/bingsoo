from discord.ui.item import Item, ItemCallbackType
import discord

# class TimeSelect(discord.ui.Select):
#     def __init__(
#         self,
#         start_time: datetime,
#         end_time: datetime,
#         paginator: When2MeetPaginator,
#         row: int,
#         placeholder: str = "Select a start time and an end time.",
#         disabled: bool = False
#     ):
#         options = []
#         for hour in range((end_time - start_time).seconds // 3600 + 1):
#             new_time = start_time + timedelta(hours=hour)
#             options.append(
#                 discord.SelectOption(
#                     label=format(new_time, '%I %p'),
#                     emoji=num_to_clock_emoji[new_time.hour % 12],
#                     value=str(hour)
#                 )
#             )

#         super().__init__(
#             placeholder=placeholder,
#             min_values=2,
#             max_values=2,
#             options=options,
#             disabled=disabled,
#             row=row
#         )

#         self.paginator = paginator
#         self.start_time = start_time
#         self.end_time = end_time

#     async def callback(self, interaction: discord.Interaction):
#         commands.info(f"{interaction.user} selected {self.values} ID: {id(self.paginator)}")
#         for option in self.options:
#             option.default = False
#             for value in self.values:
#                 if value == option.value:
#                     option.default = True

#         if len(self.values) == 2:
#             self.paginator.submit_button.disabled = False
#             await self.paginator.goto_page(1)

#     def values_as_int(self, sort: bool = True) -> List[int]:
#         values = map(lambda string: int(string), self.values)
#         return list(sorted(values) if sort else values)

#     @property
#     def earliest(self) -> int:
#         return self.values_as_int()[0]

#     @property
#     def latest(self) -> int:
#         return self.values_as_int()[1]

class ViewWithItemCallbackType(discord.ui.View):
    def __init__(self, *items: Item, timeout: float | None = 180, disable_on_timeout: bool = False, item_callback_type: list[ItemCallbackType] = None):
        if item_callback_type:
            self.__view_children_items__ += item_callback_type
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)

class ChooseClasses(discord.ui.Select):
    def __init__(
        self,
        classes: list[str],
        placeholder: str = "Choose which classes to announce",
        disabled: bool = False,
    ):
        # for course in classes:
        #     self.add_option(label=course)
        options = []
        for course in classes:
            options.append(
                discord.SelectOption(
                    label=course
                )
            )

        super().__init__(
            placeholder=placeholder,
            min_values=1,
            max_values=len(classes),
            options=options,
            row=0
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(self.values)
        # for option in self.options:
        #     option.default = False
        #     for value in self.values:
        #         if value == option.value:
        #             option.default = True

    # @discord.ui.select( # the decorator that lets you specify the properties of the select menu
    #     placeholder = "Choose classes you want announced", # the placeholder text that will be displayed if nothing is selected
    #     min_values = 1, # the minimum number of values that must be selected by the users
    #     max_values = 1, # the maximum number of values that can be selected by the users
    #     options = [ # the list of options from which users can choose, a required field
    #         discord.SelectOption(
    #             label="Vanilla",
    #             description="Pick this if you like vanilla!"
    #         ),
    #         discord.SelectOption(
    #             label="Chocolate",
    #             description="Pick this if you like chocolate!"
    #         ),
    #         discord.SelectOption(
    #             label="Strawberry",
    #             description="Pick this if you like strawberry!"
    #         )
    #     ]
    # )
    # async def select_callback(self, select, interaction): # the function called when the user is done selecting options
    #     await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")
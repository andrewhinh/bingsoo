from discord.ui.item import Item, ItemCallbackType
import functools
import discord

def convert_to_item(item_callback_type: ItemCallbackType) -> Item:
    item = item_callback_type.__discord_ui_model_type__(
        **item_callback_type.__discord_ui_model_kwargs__
    )
    item.callback = functools.partial(item_callback_type, item)
    return item


# class ViewWithItemCallbackType(discord.ui.View):
#     def __init__(self, *items: Item, timeout: float | None = 180, disable_on_timeout: bool = False, item_callback_type: list[ItemCallbackType] = None):
#         if item_callback_type:
#             self.__view_children_items__ += item_callback_type
#         super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)

class ChooseAssignments(discord.ui.Select):
    def __init__(
        self,
        classes: list[str],
        placeholder: str = "Choose which classes to show assignments from",
        disabled: bool = False,
    ):
        # for course in classes:
        #     self.add_option(label=course)
        options = []
        for course in classes:
            options.append(
                discord.SelectOption(
                    label=course,
                    default=True
                )
            )

        super().__init__(
            placeholder=placeholder,
            min_values=1,
            max_values=len(classes),
            options=options,
            row=0
        )

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
        print('callback called')
        await interaction.response.defer(invisible=True)
        print('after ping')

    # async def callback(self, interaction: discord.Interaction):
    #     await interaction.response.send_message(self.values)
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
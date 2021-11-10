import asyncio

import nextcord
from nextcord.ext import commands

from .constant import language, country_code


class Dropdown(nextcord.ui.Select):
    def ___init__(self):
        selectOptions = [
            nextcord.SelectOption(label=country_code_row, description=country) for country, country_code_row in language.items()
        ]

        super().__init__(placeholder='Country list', min_values=1, max_values=1, options=selectOptions)

class DropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(Dropdown())
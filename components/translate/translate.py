import asyncio
from googletrans import Translator

import discord
from discord.ext import commands

from .constant import language, country_code


class Translate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name='translate')
    @commands.has_role('Verified')
    async def translate(self, ctx, source: str, destination: str, *text):
        """
        Translate message and edit old message.

        Source language detect language use 'auto'.
        """

        print(source, destination, text)

        translator = Translator()

        _source = 'auto'
        _destination = 'en'
        _text = ''

        if len(' '.join(text[:])) <= 0:
            return await ctx.send('Text is a required argument that is missing.')

        if not destination.lower():
            _destination = destination
        else:
            if destination.lower() not in language.keys():
                return await ctx.send('Invalid destination language')
            elif destination.lower() not in country_code:
                return await ctx.send('Invalid destination language')
            else:
                if destination.lower() in country_code:
                    _destination = destination
                else:
                    _destination = language[destination]

        result = translator.translate(' '.join(text[:]), dest=_destination, src=_source)

        await ctx.message.edit(content=result)

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
        translator = Translator()

        _source = 'auto'
        _destination = 'en'
        _text = ''

        if len(' '.join(text[:])) <= 0:
            return await ctx.send('Text is a required argument that is missing.')

        if source.lower() == 'auto':
            _source = 'auto'
        else:
            if source.lower() in list(language.keys()) or source.lower() in country_code:
                if source.lower() in country_code:
                    _source = source
                else:
                    _source = language[source]
            else:
                return await ctx.send('Invalid source language')

        if destination.lower() in list(country.keys()) or destination.lower() in country_code:
            if destination.lower() in country_code:
                _destination = destination
            else:
                _destination = language[destination]
        else:
            return await ctx.send('Invalid destination language')

        result = translator.translate(' '.join(text[:]), dest=_destination, src=_source)

        await ctx.message.edit(content=result)

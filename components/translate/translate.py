import asyncio
from googletrans import Translator

import discord
from discord.ext import commands

from translate.constant import language


class Translate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name='translate')
    @commands.has_role('Verified')
    async def translate(self, ctx, source: str, destination: str, text: str):
        """
        Translate message and edit old message.

        Source language detect language use 'auto'.
        """
        translator = Translator()

        _source = 'auto'
        _destination = 'en'

        if not source:
            _source = translator.detect(text)
        else:
            if source not in constant.language.keys() or source == 'auto':
                return await ctx.send('Invalid source language')

        if not destination:
            _destination = destination
        else:
            if destination not in constant.language.keys():
                return await ctx.send('Invalid destination language')

        result = translator.translate(text, dest=_destination, src=_source)

        await ctx.message.edit(content=result)

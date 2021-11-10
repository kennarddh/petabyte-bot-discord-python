import asyncio
from googletrans import Translator

import nextcord
from nextcord.ext import commands

from .constant import language, country_code
from .language_support_dropdown import DropdownView


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

        if destination.lower() in list(language.keys()) or destination.lower() in country_code:
            if destination.lower() in country_code:
                _destination = destination
            else:
                _destination = language[destination]
        else:
            return await ctx.send('Invalid destination language')

        result = translator.translate(' '.join(text[:]), dest=_destination, src=_source)

        embed = nextcord.Embed(color=nextcord.Colour.blurple())

        embed.add_field(name="Original", value=' '.join(text[:]), inline=False)
        embed.add_field(name="Result", value=result.text, inline=False)
        embed.add_field(name="Source Language", value={v: k for k, v in language.items()}[_source], inline=False)
        embed.add_field(name="Destination Language", value={v: k for k, v in language.items()}[_destination], inline=False)

        await ctx.reply(embed = embed)

    @commands.command(name='translate_language_support')
    @commands.has_role('Verified')
    async def language_support(self, ctx):
        """Show language support list"""
        
        await ctx.reply(view=DropdownView())

import asyncio
from googletrans import Translator
from typing import Optional

import nextcord
from nextcord.ext import commands

from .constant import language, country_code


class Translate(commands.Cog, name='translate'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name='translate', description="Translate message and edit old message. Source language detect language use 'auto'.")
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
                    _source = source.lower()
                else:
                    _source = language[source]
            else:
                return await ctx.send('Invalid source language')

        if destination.lower() in list(language.keys()) or destination.lower() in country_code:
            if destination.lower() in country_code:
                _destination = destination.lower()
            else:
                _destination = language[destination]
        else:
            return await ctx.send('Invalid destination language')

        if _source != 'auto':
            result = translator.translate(' '.join(text[:]), dest=_destination, src=_source)
        else:
            result = translator.translate(' '.join(text[:]), dest=_destination)

        embed = nextcord.Embed(color=nextcord.Colour.blurple())

        embed.add_field(name="Original", value=' '.join(text[:]), inline=False)
        embed.add_field(name="Result", value=result.text, inline=False)
        embed.add_field(name="Source Language", value={v: k for k, v in language.items()}[result.src], inline=False)
        embed.add_field(name="Destination Language", value={v: k for k, v in language.items()}[result.dest], inline=False)

        await ctx.reply(embed = embed)

    @commands.command(name='translate_language_support', description='Show language support list')
    @commands.has_role('Verified')
    async def language_support(self, ctx):
        """Show language support list"""
        response = '```'

        response += 'country, code'

        for language_row, country_code in language.items():
            response += '\n{}, {}'.format(language_row, country_code)

        response += '\n```'

        await ctx.reply(response)

import nextcord
from nextcord.ext import commands

from ..database.database import Database

class Suggestion(commands.Cog, name='suggestion'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="suggestion_new", description="Create new suggestion")
    @commands.has_role('Verified')
    async def new(self, ctx, *, suggestion: str):
        suggestion_channel = nextcord.utils.get(ctx.guild.channels, name='petabyte-bot-suggestion')
        
        if ctx.channel != suggestion_channel:
            return await ctx.reply('This command can only be used in \'petabyte-bot-suggestion\' channel')

        database = Database()

        suggestion = database.new_suggestion(ctx.author.id, ctx.guild.id, ctx.author.name, suggestion)

        if not suggestion:
            database.close()

            return await ctx.reply('Need level 10 or above to use suggestion commands')

        embed = nextcord.Embed(title='New suggestion')

        embed.add_field(
            name='Content',
            value=suggestion['content'],
            inline=False
        )

        embed.add_field(
            name='Id',
            value=suggestion['id'],
            inline=True
        )

        embed.add_field(
            name='Status',
            value=' '.join(suggestion['status'].split('_')).title(),
            inline=True
        )

        database.close()

        return await ctx.reply('New suggestion created', embed=embed)
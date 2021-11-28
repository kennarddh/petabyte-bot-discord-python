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

        database.close()
        if not suggestion:
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

        return await ctx.reply('New suggestion created', embed=embed)

    @commands.command(name="suggestion_all_my", description="View all my suggestion")
    @commands.has_role('Verified')
    async def all_my(self, ctx):
        suggestion_channel = nextcord.utils.get(ctx.guild.channels, name='petabyte-bot-suggestion')
        
        if ctx.channel != suggestion_channel:
            return await ctx.reply('This command can only be used in \'petabyte-bot-suggestion\' channel')

        database = Database()

        suggestion = database.get_all_my_suggestion(ctx.author.id, ctx.guild.id, ctx.author.name)
        
        database.close()

        if not suggestion:
            return await ctx.reply('Need level 10 or above to use suggestion commands')

        send = '```\nId Status\n'

        for i in suggestion:
            if i['status'] != 'deleted':
                send += '{} {}\n'.format(i['id'], ' '.join(i['status'].split('_')).title())

        send += '```'

        await ctx.reply(send)

    @commands.command(name="suggestion_detail", description="View suggestion detail")
    @commands.has_role('Verified')
    async def detail(self, ctx, suggestion_id: int):
        suggestion_channel = nextcord.utils.get(ctx.guild.channels, name='petabyte-bot-suggestion')
        
        if ctx.channel != suggestion_channel:
            return await ctx.reply('This command can only be used in \'petabyte-bot-suggestion\' channel')

        database = Database()

        suggestion = database.get_suggestion_detail(ctx.author.id, ctx.guild.id, ctx.author.name, suggestion_id)
        
        database.close()

        if not suggestion:
            return await ctx.reply('Need level 10 or above to use suggestion commands')

        if suggestion == 'no_suggestion':
            return await ctx.reply('No suggestions with id {}'.format(suggestion_id))

        embed = nextcord.Embed(title='Suggestion detail')

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

        return await ctx.reply('Suggestion detail', embed=embed)

    @commands.command(name="suggestion_approve", description="Approve suggestion")
    @commands.has_role('Petabyte bot manager')
    @commands.has_role('Verified')
    async def approve(self, ctx, suggestion_id: int):
        suggestion_channel = nextcord.utils.get(ctx.guild.channels, name='petabyte-bot-suggestion')
        
        if ctx.channel != suggestion_channel:
            return await ctx.reply('This command can only be used in \'petabyte-bot-suggestion\' channel')

        database = Database()

        suggestion = database.get_suggestion_detail(ctx.author.id, ctx.guild.id, ctx.author.name, suggestion_id)

        if suggestion == 'no_suggestion':
            return await ctx.reply('No suggestions with id {}'.format(suggestion_id))

        result = database.approve_suggestion(ctx.author.id, ctx.guild.id, ctx.author.name, suggestion_id)

        suggestion = database.get_suggestion_detail(ctx.author.id, ctx.guild.id, ctx.author.name, suggestion_id)

        database.close()

        if not result:
            return await ctx.reply('Suggestion already approved')

        embed = nextcord.Embed(title='Suggestion approved')

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

        return await ctx.reply('Suggestion aproved', embed=embed)

    @commands.command(name="suggestion_decline", description="Decline suggestion")
    @commands.has_role('Petabyte bot manager')
    @commands.has_role('Verified')
    async def decline(self, ctx, suggestion_id: int):
        suggestion_channel = nextcord.utils.get(ctx.guild.channels, name='petabyte-bot-suggestion')
        
        if ctx.channel != suggestion_channel:
            return await ctx.reply('This command can only be used in \'petabyte-bot-suggestion\' channel')

        database = Database()

        suggestion = database.get_suggestion_detail(ctx.author.id, ctx.guild.id, ctx.author.name, suggestion_id)

        if suggestion == 'no_suggestion':
            return await ctx.reply('No suggestions with id {}'.format(suggestion_id))

        result = database.decline_suggestion(ctx.author.id, ctx.guild.id, ctx.author.name, suggestion_id)

        suggestion = database.get_suggestion_detail(ctx.author.id, ctx.guild.id, ctx.author.name, suggestion_id)

        database.close()

        if not result:
            return await ctx.reply('Suggestion already declined')

        embed = nextcord.Embed(title='Suggestion declined')

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

        return await ctx.reply('Suggestion declined', embed=embed)

    @commands.command(name="suggestion_delete", description="Delete suggestion")
    @commands.has_role('Verified')
    async def delete(self, ctx, suggestion_id: int):
        suggestion_channel = nextcord.utils.get(ctx.guild.channels, name='petabyte-bot-suggestion')
        
        if ctx.channel != suggestion_channel:
            return await ctx.reply('This command can only be used in \'petabyte-bot-suggestion\' channel')

        database = Database()

        user = database.get_user(ctx.author.id, ctx.author.name, ctx.guild.id)

        suggestion = database.get_suggestion_detail(ctx.author.id, ctx.guild.id, ctx.author.name, suggestion_id)

        if suggestion == 'no_suggestion':
            return await ctx.reply('No suggestions with id {}'.format(suggestion_id))
            
        if suggestion['user_id'] != user['id']:
            return await ctx.reply('You are not the author of this suggestion')

        result = database.delete_suggestion(ctx.author.id, ctx.guild.id, ctx.author.name, suggestion_id)

        suggestion = database.get_suggestion_detail(ctx.author.id, ctx.guild.id, ctx.author.name, suggestion_id)

        database.close()

        if not result:
            return await ctx.reply('Suggestion already deleted')

        return await ctx.reply('Suggestion deleted')

    @commands.command(name="suggestion_all", description="View all suggestion")
    @commands.has_role('Petabyte bot manager')
    @commands.has_role('Verified')
    async def all(self, ctx):
        suggestion_channel = nextcord.utils.get(ctx.guild.channels, name='petabyte-bot-suggestion')
        
        if ctx.channel != suggestion_channel:
            return await ctx.reply('This command can only be used in \'petabyte-bot-suggestion\' channel')

        database = Database()

        suggestion = database.get_all_suggestion(ctx.author.id, ctx.guild.id, ctx.author.name)
        
        database.close()

        if not suggestion:
            return await ctx.reply('Need level 10 or above to use suggestion commands')

        send = '```\nId Status\n'

        for i in suggestion:
            if i['status'] != 'deleted':
                send += '{} {}\n'.format(i['id'], ' '.join(i['status'].split('_')).title())

        send += '```'

        await ctx.reply(send)

import nextcord
from nextcord.ext import commands

from ..database.database import Database

class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        database = Database()

        if not database.check_user_exist(message.author.id, message.guild.id):
            database.create_user(message.author.id, message.author.name, message.guild.id)

        database.level_up(message.author.id, message.guild.id, 10)

        database.close()

    @commands.command(name='my_stats', description='Show my stats')
    @commands.has_role('Verified')
    async def my_stats(self, ctx):
        database = Database()

        if not database.check_user_exist(ctx.author.id, ctx.guild.id):
            database.create_user(ctx.author.id, ctx.author.name, ctx.guild.id)
        
        my_stats_result = database.get_user_stats(ctx.author.id, ctx.guild.id)

        database.close()

        embed = nextcord.Embed(title='My stats')

        embed.add_field(
            name='Level',
            value=my_stats_result['level']
        )
        
        embed.add_field(
            name='Level',
            value=my_stats_result['experience']
        )

        await ctx.reply(embed=embed)

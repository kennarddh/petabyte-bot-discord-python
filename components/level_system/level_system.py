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
            database.create_user(message.author.id, message.guild.id)

        database.level_up(message.author.id, message.guild.id, 10)

        database.commit()
        database.close()
        
        await bot.process_commands(message)
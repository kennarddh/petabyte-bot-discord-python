import os
import asyncio

import nextcord
from nextcord.ext import commands, tasks
from nextcord.utils import get
from dotenv import load_dotenv

# components
from components import music, error_handler, admin_commands, public_commands, translate, level_system, suggestion


load_dotenv()
TOKEN = os.environ['DISCORD_TOKEN']

intents = nextcord.Intents().all()

bot = commands.Bot(command_prefix='!', intents=intents)


bot.remove_command('help')

# cog
bot.add_cog(music.Music(bot))
bot.add_cog(error_handler.CommandErrorHandler(bot))
bot.add_cog(admin_commands.AdminCommands(bot))
bot.add_cog(public_commands.PublicCommands(bot))
bot.add_cog(translate.translate.Translate(bot))
bot.add_cog(level_system.level_system.LevelSystem(bot))
bot.add_cog(suggestion.suggestion.Suggestion(bot))

@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

        ownerRole = nextcord.utils.find(lambda r: r.name == 'Owner', guild.roles)
        verifiedRole = nextcord.utils.find(lambda r: r.name == 'Verified', guild.roles)
        verifyChannel = nextcord.utils.get(guild.channels, name="verify")
        confirmEmoji = '\U00002705'
        
        await verifyChannel.purge(limit=100)

        message = await verifyChannel.send("Click reaction to verify")
        
        await message.add_reaction(emoji = confirmEmoji)

        @bot.event
        async def on_reaction_add(reaction, user):
            if reaction.emoji == confirmEmoji:
                if ownerRole not in user.roles:
                    if verifiedRole not in user.roles:
                        channel = nextcord.utils.get(guild.channels, name="welcome")

                        await channel.send(f'Hi {user.name}, welcome to Petabyte server!')

                        await user.add_roles(verifiedRole)

                        await user.create_dm()
                        await user.dm_channel.send(
                            f'Hi {user.name}, welcome to Petabyte server!'
                        )


bot.run(TOKEN)

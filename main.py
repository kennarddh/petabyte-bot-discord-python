import os
import asyncio

import discord
from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv

# components
from components import music, error_handler, admin_commands, public_commands


load_dotenv()
TOKEN = os.environ['DISCORD_TOKEN']

intents = discord.Intents().all()

help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

bot = commands.Bot(command_prefix='!', intents=intents)


# cog
bot.add_cog(music.Music(bot))
bot.add_cog(error_handler.CommandErrorHandler(bot))
bot.add_cog(admin_commands.AdminCommands(bot))
bot.add_cog(public_commands.PublicCommands(bot))

@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

        ownerRole = discord.utils.find(lambda r: r.name == 'Owner', guild.roles)
        verifiedRole = discord.utils.find(lambda r: r.name == 'Verified', guild.roles)
        verifyChannel = discord.utils.get(guild.channels, name="verify")
        confirmEmoji = '\U00002705'
        
        await verifyChannel.purge(limit=100)

        message = await verifyChannel.send("Click reaction to verify")
        
        await message.add_reaction(emoji = confirmEmoji)

        @bot.event
        async def on_reaction_add(reaction, user):
            if reaction.emoji == confirmEmoji:
                if ownerRole not in user.roles:
                    if verifiedRole not in user.roles:
                        channel = discord.utils.get(guild.channels, name="welcome")

                        await channel.send(f'Hi {user.name}, welcome to Petabyte server!')

                        await user.add_roles(verifiedRole)

                        await member.create_dm()
                        await member.dm_channel.send(
                            f'Hi {member.name}, welcome to Petabyte server!'
                        )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)


bot.run(TOKEN)

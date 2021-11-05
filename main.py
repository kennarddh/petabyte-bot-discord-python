import os
import asyncio
import time

import discord
from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.environ['DISCORD_TOKEN']

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.members = True

help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to Petabyte server!'
    )

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    role = discord.utils.find(lambda r: r.name == 'Verified', message.author.guild.roles)

    if role in message.author.roles:
        await bot.process_commands(message)

@bot.command(name="mute", help="Mute Member Command : '!mute {member}'")
@commands.has_any_role('Petabyte bot manager')
async def mute(ctx, member : discord.Member):
    await member.edit(mute=True)
    
    ctx.channel.send("Succesfully Muted {}".format(member.name))

@bot.command(name="unmute", help="Unmute Member Command : '!unmute {member}'")
@commands.has_any_role('Petabyte bot manager')
async def unmute(ctx, member : discord.Member):
    await member.edit(mute=False)

    ctx.channel.send("Succesfully Unmuted {}".format(member.name))

@bot.command(name="verify", help="Verify To Chat In This Server")
async def verify(ctx):
    confirmEmoji = '\U00002705'
    
    message = await ctx.send("Click reaction to verify\nTimeout 30 second")
    
    await message.add_reaction(emoji=confirmEmoji)

    def check(reaction, user):
        return reaction.emoji == confirmEmoji

    reaction, user = await bot.wait_for('reaction_add', timeout=30, check=check)

    channel = discord.utils.get(member.guild.channels, name="welcome")

    channel_id = channel.id

    await bot.get_channel(channel_id).send(f'Hi {member.name}, welcome to Petabyte server!')

    roleToAdd = get(ctx.guild.roles, name="Verified")

    memberToAddRole = get(ctx.guild.members,name=ctx.author.name)

    await memberToAddRole.add_roles(roleToAdd)

    await message.delete()

@bot.command(name="purgeChannel", help="Purge channel with limit Command : '!purgeChannel {Limit(int)}'")
@commands.has_any_role('Petabyte bot manager')
async def purgeChannel(ctx, limit : int):
    await ctx.channel.purge(limit=limit)

@bot.command(name="resetNick", help="Reset Member Nickname Command : '!resetNick {@Member}'")
@commands.has_any_role('Petabyte bot manager')
async def resetNick(ctx, member : discord.Member):
    memberNick = member.nick

    if memberNick == None:
        memberNick = member.name
    
    memberName = member.name
    await member.edit(nick=memberName)

    await ctx.channel.send("{} Nickname Has Been Successfully Changed To {}".format(memberNick, memberName))

@bot.command(name="resetAllNick", help="Reset All Member Nickname In Server Command : '!resetAllNick'")
@commands.has_any_role('Petabyte bot manager')
async def resetAllNick(ctx):
    guild = ctx.guild
    members = guild.members

    response = "Successfully Changed All Member Nickname\nOld To New\n"

    for member in members:
        if member != guild.owner:
            memberNick = member.nick

            if memberNick == None:
                memberNick = member.name

            memberName = member.name
            await member.edit(nick=memberName)

    await ctx.channel.send("Successfully Changed All Member Nickname\nOld To New")

@bot.command(name="ping", help="Send Ping Command : '!ping'")
@commands.has_any_role('Petabyte bot manager')
async def ping(ctx):
    before = time.monotonic()
    
    message = await ctx.channel.send("Pong!")

    ping = (time.monotonic() - before) * 1000

    await message.edit(content="Ping! `{}ms`".format(int(ping)))
    
bot.run(TOKEN)

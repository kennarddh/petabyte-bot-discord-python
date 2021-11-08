import os
import asyncio
import time

import discord
from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv

# components
from components import music, error_handler


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


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to Petabyte server!'
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)


# admin commands

@bot.command(name="mute", help="Mute Member Command : '!mute {member}'")
@commands.has_role('Petabyte bot manager')
@commands.has_role('Verified')
async def mute(ctx, member : discord.Member):
    ownerRole = discord.utils.find(lambda r: r.name == 'Owner', ctx.message.guild.roles)
    if ownerRole not in member.roles:
        await member.edit(mute=True)
        
        ctx.channel.send("Succesfully Muted {}".format(member.name))
    else:
        await ctx.send("Can't modify owner")

@bot.command(name="unmute", help="Unmute Member Command : '!unmute {member}'")
@commands.has_role('Petabyte bot manager')
@commands.has_role('Verified')
async def unmute(ctx, member : discord.Member):
    ownerRole = discord.utils.find(lambda r: r.name == 'Owner', ctx.message.guild.roles)
    if ownerRole not in member.roles:
        await member.edit(mute=False)

        ctx.channel.send("Succesfully Unmuted {}".format(member.name))
    else:
        await ctx.send("Can't modify owner")

@bot.command(name="purge", help="Purge channel with limit Command : '!purgeChannel {Limit(int)}'")
@commands.has_role('Petabyte bot manager')
@commands.has_role('Verified')
async def purge(ctx, limit : int):
    await ctx.channel.purge(limit=limit)

@bot.command(name="resetNick", help="Reset Member Nickname Command : '!resetNick {@Member}'")
@commands.has_role('Petabyte bot manager')
@commands.has_role('Verified')
async def resetNick(ctx, member : discord.Member):
    ownerRole = discord.utils.find(lambda r: r.name == 'Owner', ctx.message.guild.roles)
    if ownerRole not in member.roles:
        memberNick = member.nick

        if memberNick == None:
            memberNick = member.name
        
        memberName = member.name
        await member.edit(nick=memberName)

        await ctx.channel.send("{} Nickname Has Been Successfully Changed To {}".format(memberNick, memberName))
    else:
        await ctx.send("Can't modify owner")

@bot.command(name="resetAllNick", help="Reset All Member Nickname In Server Command : '!resetAllNick'")
@commands.has_role('Petabyte bot manager')
@commands.has_role('Verified')
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
            await member.edit(nick = memberName)

    await ctx.channel.send("Successfully Changed All Member Nickname\nOld To New")


# public commands

@bot.command(name="ping", help="Send Ping Command : '!ping'")
@commands.has_role('Verified')
async def ping(ctx):
    await ctx.send('My ping is {}s'.format(round(bot.latency, 1)))

@bot.command(name="where_am_i", help="Prints details of Server")
@commands.has_role('Verified')
@commands.guild_only()
async def where_am_i(ctx):
    owner = str(ctx.guild.owner)
    region = str(ctx.guild.region)
    guild_id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    desc = ctx.guild.description
    

    if desc:
        embed = discord.Embed(
            title = ctx.guild.name + " Server Information",
            description = desc,
            color = discord.Color.blue()
        )
    else:
        embed = discord.Embed(
            title = ctx.guild.name + " Server Information",
            description = "No description",
            color = discord.Color.blue()
        )


    embed.set_thumbnail(url = icon)
    embed.add_field(name = "Owner", value = owner, inline = True)
    embed.add_field(name = "Server ID", value = guild_id, inline = True)
    embed.add_field(name = "Region", value = region, inline = True)
    embed.add_field(name = "Member Count", value = memberCount, inline = True)

    await ctx.send(embed = embed)


bot.run(TOKEN)

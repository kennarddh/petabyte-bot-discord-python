import asyncio

import discord

from discord.ext import commands


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mute", help="Mute Member Command : '!mute {member}'")
    @commands.has_role('Petabyte bot manager')
    @commands.has_role('Verified')
    async def mute(self, ctx, member : discord.Member):
        ownerRole = discord.utils.find(lambda r: r.name == 'Owner', ctx.message.guild.roles)
        if ownerRole not in member.roles:
            await member.edit(mute=True)
            
            ctx.channel.send("Succesfully Muted {}".format(member.name))
        else:
            await ctx.send("Can't modify owner")

    @commands.command(name="unmute", help="Unmute Member Command : '!unmute {member}'")
    @commands.has_role('Petabyte bot manager')
    @commands.has_role('Verified')
    async def unmute(self, ctx, member : discord.Member):
        ownerRole = discord.utils.find(lambda r: r.name == 'Owner', ctx.message.guild.roles)
        if ownerRole not in member.roles:
            await member.edit(mute=False)

            ctx.channel.send("Succesfully Unmuted {}".format(member.name))
        else:
            await ctx.send("Can't modify owner")

    @commands.command(name="purge", help="Purge channel with limit Command : '!purgeChannel {Limit(int)}'")
    @commands.has_role('Petabyte bot manager')
    @commands.has_role('Verified')
    async def purge(self, ctx, limit : int):
        await ctx.channel.purge(limit=limit)

    @commands.command(name="resetNick", help="Reset Member Nickname Command : '!resetNick {@Member}'")
    @commands.has_role('Petabyte bot manager')
    @commands.has_role('Verified')
    async def resetNick(self, ctx, member : discord.Member):
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

    @commands.command(name="resetAllNick", help="Reset All Member Nickname In Server Command : '!resetAllNick'")
    @commands.has_role('Petabyte bot manager')
    @commands.has_role('Verified')
    async def resetAllNick(self, ctx):
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

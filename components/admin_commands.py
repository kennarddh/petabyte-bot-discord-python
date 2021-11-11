import asyncio
from typing import Optional

import nextcord

from nextcord.ext import commands


class AdminCommands(commands.Cog, name='Admin commands'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mute", description="Mute Member")
    @commands.has_role('Petabyte bot manager')
    @commands.has_role('Verified')
    async def mute(self, ctx, member : nextcord.Member):
        ownerRole = nextcord.utils.find(lambda r: r.name == 'Owner', ctx.message.guild.roles)
        if ownerRole not in member.roles:
            await member.edit(mute=True)
            
            ctx.channel.send("Succesfully Muted {}".format(member.name))
        else:
            await ctx.send("Can't modify owner")

    @commands.command(name="unmute", description="Unmute Member")
    @commands.has_role('Petabyte bot manager')
    @commands.has_role('Verified')
    async def unmute(self, ctx, member : nextcord.Member):
        ownerRole = nextcord.utils.find(lambda r: r.name == 'Owner', ctx.message.guild.roles)
        if ownerRole not in member.roles:
            await member.edit(mute=False)

            ctx.channel.send("Succesfully Unmuted {}".format(member.name))
        else:
            await ctx.send("Can't modify owner")

    @commands.command(name="purge", description="Purge channel with limit")
    @commands.has_role('Petabyte bot manager')
    @commands.has_role('Verified')
    async def purge(self, ctx, limit : int):
        await ctx.channel.purge(limit=limit)

    @commands.command(name="reset_nick", description="Reset Member Nickname")
    @commands.has_role('Petabyte bot manager')
    @commands.has_role('Verified')
    async def resetNick(self, ctx, member : nextcord.Member):
        ownerRole = nextcord.utils.find(lambda r: r.name == 'Owner', ctx.message.guild.roles)
        if ownerRole not in member.roles:
            memberNick = member.nick

            if memberNick == None:
                memberNick = member.name
            
            memberName = member.name
            await member.edit(nick=memberName)

            await ctx.channel.send("{} Nickname Has Been Successfully Changed To {}".format(memberNick, memberName))
        else:
            await ctx.send("Can't modify owner")

    @commands.command(name="reset_all_nick", description="Reset All Member Nickname In Server")
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

    @commands.command(name="lock", description="Lock channel or server")
    @commands.has_role('Petabyte bot manager')
    @commands.has_role('Verified')
    async def lock(self, ctx, channel: nextcord.TextChannel = None, setting = None):
        verified_role = nextcord.utils.get(ctx.guild.roles, name="Verified")

        if setting == '--server':
            for channel in ctx.guild.channels:
                await channel.set_permissions(verified_role, reason='{} locked {} with --server'.format(ctx.author.name, channel.name), send_messages=False)
            
            return await ctx.send('Locked server down')

        if channel is None:
            channel = ctx.message.channel

        await channel.set_permissions(verified_role, reason='{} locked {}'.format(ctx.author.name, channel.name), send_messages=False)
        await ctx.send('Locked channel down')

    @commands.command(name="unlock", description="Unlock channel or server")
    @commands.has_role('Petabyte bot manager')
    @commands.has_role('Verified')
    async def unlock(self, ctx, channel: nextcord.TextChannel = None, setting = None):
        verified_role = nextcord.utils.get(ctx.guild.roles, name="Verified")
        
        if setting == '--server':
            for channel in ctx.guild.channels:
                await channel.set_permissions(verified_role, reason='{} unlocked {} with --server'.format(ctx.author.name, channel.name), send_messages=True)
            
            return await ctx.send('Unlocked server')

        if channel is None:
            channel = ctx.message.channel

        await channel.set_permissions(verified_role, reason='{} unlocked {}'.format(ctx.author.name, channel.name), send_messages=True)
        await ctx.send('Unlocked channel')

import asyncio

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

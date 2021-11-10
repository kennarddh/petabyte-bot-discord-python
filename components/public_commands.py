import asyncio

import nextcord

from nextcord.ext import commands


class PublicCommands(commands.Cog, name='Public commands'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", help="Send Ping Command : '!ping'")
    @commands.has_role('Verified')
    async def ping(self, ctx):
        await ctx.send('My ping is {}s'.format(round(self.bot.latency, 1)))

    @commands.command(name="where_am_i", help="Prints details of Server")
    @commands.has_role('Verified')
    @commands.guild_only()
    async def where_am_i(self, ctx):
        owner = str(ctx.guild.owner)
        region = str(ctx.guild.region)
        guild_id = str(ctx.guild.id)
        memberCount = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon_url)
        desc = ctx.guild.description
        

        if desc:
            embed = nextcord.Embed(
                title = ctx.guild.name + " Server Information",
                description = desc,
                color = nextcord.Color.blue()
            )
        else:
            embed = nextcord.Embed(
                title = ctx.guild.name + " Server Information",
                description = "No description",
                color = nextcord.Color.blue()
            )


        embed.set_thumbnail(url = icon)
        embed.add_field(name = "Owner", value = owner, inline = True)
        embed.add_field(name = "Server ID", value = guild_id, inline = True)
        embed.add_field(name = "Region", value = region, inline = True)
        embed.add_field(name = "Member Count", value = memberCount, inline = True)

        await ctx.send(embed = embed)

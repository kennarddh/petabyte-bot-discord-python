import asyncio
from typing import Optional

import nextcord

from nextcord.ext import commands


class PublicCommands(commands.Cog, name='Public commands'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", description="Bot latency")
    @commands.has_role('Verified')
    async def ping(self, ctx):
        await ctx.send('My ping is {}s'.format(round(self.bot.latency, 1)))

    @commands.command(name="where_am_i", description="Prints details of Server")
    @commands.has_role('Verified')
    @commands.guild_only()
    async def where_am_i(self, ctx):
        owner = str(ctx.guild.owner)
        region = str(ctx.guild.region)
        guild_id = str(ctx.guild.id)
        memberCount = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon)
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

    @commands.command(name="help", description='Show help')
    @commands.has_role('Verified')
    @commands.guild_only()
    async def help(self, ctx, command_or_category: Optional[str]):
        """Show help"""

        embed = nextcord.Embed(title='Petabyte\'s help', description='Help command for Petabyte bot')

        before_category = None
        no_category = 'No category'

        help_data = {}
        all_command = {}

        for command in self.bot.walk_commands():
            description = command.description

            if before_category != command.cog.qualified_name or before_category is None:
                before_category = command.cog.qualified_name if command.cog is not None else no_category

            if not description or description is None or description == '':
                description = 'No description provided'

            if before_category not in help_data:
                help_data[before_category] = []

            help_data[before_category].append({
                'name': command.name,
                'signature': command.signature if command.signature is not None else '',
                'description': description
            })

            all_command[command.name.lower()] = {
                'name': command.name,
                'signature': command.signature if command.signature is not None else '',
                'description': description
            }
            
        print(help_data)
        print(all_command)

        print(['_'.join([e.lower() for e in i.split()]) for i in list(help_data.keys())])

        if not command_or_category:
            for category, command_list in help_data.items():
                embed.add_field(
                    name='{}'.format(category),
                    value='\u200b',
                    inline=False
                )

                for command in command_list:
                    embed.add_field(
                        name='{}{} {}'.format(
                            self.bot.command_prefix,
                            command['name'],
                            command['signature']
                        ),
                        value=command['description'],
                        inline=False
                    )
        elif command_or_category:
            if str(command_or_category).lower() in all_command.keys():
                embed.add_field(
                    name='{}{} {}'.format(
                        self.bot.command_prefix,
                        all_command[str(command_or_category).lower()]['name'],
                        all_command[str(command_or_category).lower()]['signature']
                    ),
                    value=all_command[str(command_or_category).lower()]['description'],
                    inline=False
                )
            elif str(command_or_category).lower() in ['_'.join([e.lower() for e in i.split()]) for i in list(help_data.keys())]:
                embed.add_field(
                    name='{}{} {}'.format(
                        self.bot.command_prefix,
                        help_data[str(command_or_category).lower()]['name'],
                        help_data[str(command_or_category).lower()]['signature']
                    ),
                    value=help_data[str(command_or_category).lower()]['description'],
                    inline=False
                )
            else:
                embed.add_field(
                    name='Error',
                    value='Invalid command or category',
                    inline=False
                )

        await ctx.reply(embed=embed)

import asyncio

import discord
import youtube_dl

from discord.ext import commands


youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog, name='Music'):
    def __init__(self, bot):
        self.bot = bot
        self.now_playing = ""
        self.volume = 0.5
        self.status = 'stop'
        self.now_url = ''

    @commands.command(name="music_join")
    @commands.has_role('Petabyte bot manager')
    @commands.has_role('Verified')
    async def join(self, ctx):
        """Joins a voice channel"""

        self.status = 'joined'

        channel = discord.utils.find(lambda c: c.name == 'Petabyte Music', ctx.author.guild.channels)
        
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command(name="music_play")
    @commands.has_role('Petabyte bot manager')
    @commands.has_role('Verified')
    async def play(self, ctx, *, url):
        """Streams from a url"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        self.now_playing = player.title
        self.status = 'playing'
        self.now_url = 'url'

        await ctx.send(f'Now playing: {player.title}')
        
    @commands.command(name="music_volume")
    @commands.has_role('Petabyte bot manager')
    @commands.has_role('Verified')
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        self.volume = volume / 100

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command(name='music_pause')
    @commands.has_role('Petabyte bot manager')
    @commands.has_role('Verified')
    async def pause(self, ctx):
        self.status = 'paused'

        voice_client = ctx.message.guild.voice_client
        
        if voice_client.is_playing():
            voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")
        
    @commands.command(name='music_resume')
    @commands.has_role('Petabyte bot manager')
    @commands.has_role('Verified')
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client

        if voice_client.is_paused():
            voice_client.resume()
        else:
            await ctx.send("The bot was not playing anything before this. Use play_song command")
        
        self.status = 'playing'

    @commands.command(name="music_stop")
    @commands.has_role('Petabyte bot manager')
    @commands.has_role('Verified')
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        self.status = 'stop'
        self.now_url = ''
        self.now_playing = ''

        await ctx.voice_client.disconnect()

    @commands.command(name="music_status")
    @commands.has_role('Verified')
    async def now_playing(self, ctx):
        print('self.now_url')
        print(self.now_url)
        if self.now_playing:
            embed = discord.Embed(
                title = "Now playing",
                colour = discord.Colour(0x5865f2),
                description = self.now_playing,
                url = self.now_url
            )
        else:
            embed = discord.Embed(
                title = "Now playing",
                colour = discord.Colour(0x5865f2),
                description = "No music is playing now"
            )

        embed.add_field(name="Volume", value="{}%".format(self.volume * 100), inline=True)
        embed.add_field(name="Status", value=self.status.capitalize(), inline=True)

        await ctx.send(embed=embed)

    @play.before_invoke
    async def ensure_voice(self, ctx):
        channel = discord.utils.find(lambda c: c.name == 'Petabyte Music', ctx.author.guild.channels)

        if ctx.voice_client is None:
            await channel.connect()
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
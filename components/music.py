import asyncio

import discord
import youtube_dl

from discord.ext import commands


youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'outtmpl': '/music/%(title)s.%(ext)s',
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
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options, executable="./ffmpeg/bin/ffmpeg.exe"), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="music_join")
    @commands.has_any_role('Petabyte bot manager')
    async def join(self, ctx):
        """Joins a voice channel"""

        channel = discord.utils.find(lambda c: c.name == 'Petabyte Music', ctx.author.guild.channels)
        
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command(name="music_play")
    @commands.has_any_role('Petabyte bot manager')
    async def play(self, ctx, *, url):
        """Streams from a url"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command(name="music_volume")
    @commands.has_any_role('Petabyte bot manager')
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command(name='music_pause')
    @commands.has_any_role('Petabyte bot manager')
    async def pause(self, ctx):
        voice_client = ctx.message.guild.voice_client
        
        if voice_client.is_playing():
            voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")
        
    @commands.command(name='music_resume')
    @commands.has_any_role('Petabyte bot manager')
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client

        if voice_client.is_paused():
            voice_client.resume()
        else:
            await ctx.send("The bot was not playing anything before this. Use play_song command")

    @commands.command(name="music_stop")
    @commands.has_any_role('Petabyte bot manager')
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    async def ensure_voice(self, ctx):
        channel = discord.utils.find(lambda c: c.name == 'Petabyte Music', ctx.author.guild.channels)

        if ctx.voice_client is None:
            await channel.connect()
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
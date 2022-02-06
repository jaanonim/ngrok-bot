import os

import discord
from discord.ext.commands.bot import Bot
from dotenv import load_dotenv

from ngrok import Ngrok
from settings import Settings

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = Bot(command_prefix="$", intents=intents)


def get_chanels():
    list = Settings().get("channels")
    if list is None:
        return []
    channels = []
    for item in list:
        guild = discord.utils.get(bot.guilds, id=item["guild"])
        channel = discord.utils.get(guild.channels, id=item["channel"])
        channels.append(channel)
    return channels


@bot.event
async def on_ready():
    print("Running!")
    for chanel in get_chanels():
        embed = discord.Embed(
            title="Server",
            description=f"New addres \n `{Ngrok().getAddres()}`",
            color=discord.Color.blue(),
        )
        await chanel.send(embed=embed)


@bot.command(pass_context=True, aliases=["author"], description="Aboute bot")
async def aboute(ctx):
    embed = discord.Embed(
        title="Aboute",
        description="Author: jaanonim",
        color=discord.Color.green(),
    )
    await ctx.send(embed=embed)


@bot.command(
    pass_context=True,
    aliases=["set", "channel"],
    description="Register channel as addres target",
)
async def set_channel(ctx, channel: discord.TextChannel = None):
    if not channel:
        embed = discord.Embed(
            title="Channel",
            description=f"Invalid channel!",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return

    c = Settings().get("channels")
    if c is None:
        c = []
    c.append({"guild": ctx.guild.id, "channel": channel.id})
    Settings().set("channels", c)

    embed = discord.Embed(
        title="Channel",
        description=f"Channel set to {channel.mention}",
        color=discord.Color.green(),
    )
    await ctx.send(embed=embed)


@bot.command(
    pass_context=True,
    aliases=["unset", "remove"],
    description="Unregister channel as addres target",
)
async def unset_channel(ctx, channel: discord.TextChannel = None):
    if not channel:
        embed = discord.Embed(
            title="Channel",
            description=f"Invalid channel!",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return

    c = Settings().get("channels")
    try:
        c.remove({"guild": ctx.guild.id, "channel": channel.id})
    except ValueError:
        embed = discord.Embed(
            title="Channel",
            description=f"This channel isn't in register!",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
    Settings().set("channels", c)

    embed = discord.Embed(
        title="Channel",
        description=f"Channel {channel.mention} unregistered",
        color=discord.Color.green(),
    )
    await ctx.send(embed=embed)


@bot.command(pass_context=True, aliases=["c", "ha"], description="Give random color")
async def color(ctx):
    guild = ctx.guild
    user = ctx.author
    role = discord.utils.get(guild.roles, name=user.name)
    if not role:
        role = await guild.create_role(name=user.name)
    c = discord.Colour.random()
    await role.edit(color=c)
    await user.add_roles(role)
    embed = discord.Embed(
        title="Colors",
        description=f"{ctx.author.mention} have new color! ✨",
        color=c,
    )
    await ctx.send(embed=embed)


if __name__ == "__main__":
    p = input("Podaj port: ")
    Ngrok().init(p)
    bot.run(TOKEN)

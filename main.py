from os import getenv

from discord import Activity, ActivityType, Color, Embed, User
from discord import __version__ as discord_version
from discord.ext.commands import Bot
from dotenv import load_dotenv

__version__ = "1.1.0"

load_dotenv()
bot = Bot(
    command_prefix="m!",
    case_insensitive=True,
    activity=Activity(type=ActivityType.watching, name="m!help"),
)


@bot.event
async def on_ready():
    print(
        f"\nSuccessfully logged in!\n\nUser: {bot.user} ({bot.user.id})\n\nModmail {__version__}\ndiscord.py {discord_version}"
    )


@bot.event
async def on_message(message):
    ctx = await bot.get_context(message)
    if ctx.command:
        await bot.invoke(ctx)
        return
    if message.guild or message.author.bot:
        return
    else:
        channel = await bot.fetch_channel(getenv("MODMAIL_CHANNEL"))
        embed = Embed(title=message.content, color=Color.gold())
        embed.set_author(name=str(message.author), icon_url=message.author.avatar_url)
        await channel.send("", embed=embed)


@bot.command(aliases=["message", "dm"])
async def msg(ctx, user: User, *, message: str):
    """
    Sends an anonymous message to a user
    """

    channel = await bot.fetch_channel(getenv("MODMAIL_CHANNEL"))
    if ctx.author.permissions_in(channel).read_messages:
        embed = Embed(title=message)
        embed.set_author(name=ctx.guild.name)
        await user.send("", embed=embed)
        await ctx.send("", embed=Embed(title="Message sent!", color=Color.gold()))
    else:
        await ctx.send(
            "",
            embed=Embed(
                title="Sorry, you can't use that command here.", color=Color.red()
            ),
        )


bot.run(getenv("BOT_DISCORD_KEY"))

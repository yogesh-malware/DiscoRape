import discord
import asyncio
from discord.ext import commands
import nekos
import random


class nsfw(commands.Cog):
    """nfsw messages"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def neko(self, ctx, message):
        """Shows a random pic of hentai u choose"""
        await ctx.delete()
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        msg = message
        embed = discord.Embed(
            title=":flushed:", description="", colour=discord.Colour.from_rgb(r, g, b),
        )
        url = nekos.img(msg)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command()
    async def nekoalt(self, ctx):
        """Shows all options for neko"""
        await ctx.delete()
        possible = [
            "feet",
            "yuri",
            "trap",
            "futanari",
            "hololewd",
            "lewdkemo",
            "solog",
            "feetg",
            "cum",
            "erokemo",
            "les",
            "wallpaper",
            "lewdk",
            "ngif",
            "tickle",
            "lewd",
            "feed",
            "gecg",
            "eroyuri",
            "eron",
            "cum_jpg",
            "bj",
            "nsfw_neko_gif",
            "solo",
            "kemonomimi",
            "nsfw_avatar",
            "gasm",
            "poke",
            "anal",
            "slap",
            "hentai",
            "avatar",
            "erofeet",
            "holo",
            "keta",
            "blowjob",
            "pussy",
            "tits",
            "holoero",
            "lizard",
            "pussy_jpg",
            "pwankg",
            "classic",
            "kuni",
            "waifu",
            "pat",
            "8ball",
            "kiss",
            "femdom",
            "neko",
            "spank",
            "cuddle",
            "erok",
            "fox_girl",
            "boobs",
            "random_hentai_gif",
            "smallboobs",
            "hug",
            "ero",
            "smug",
            "goose",
            "baka",
            "woof",
        ]

        list = ""
        for item in possible:
            print(item)

            list += f"{item}\n"

        await ctx.send(f"List of avialiable options.\n{list}")


### Add cog lmao
def setup(bot):
    bot.add_cog(nsfw(bot))

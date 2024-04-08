import re

import disnake
from disnake.ext import commands

static_re = re.compile(r"<:([^:]+):(\d+)>")
animated_re = re.compile(r"<a:([^:]+):(\d+)>")


class UtilCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["firstmes"])
    async def firstmessage(
        self, ctx: commands.Context, channel: disnake.TextChannel = None
    ):
        if channel is None:
            channel = ctx.channel
        first_message = (await channel.history(limit=1, oldest_first=True).flatten())[0]
        embed = disnake.Embed(
            title=f"First Message in {channel.name}: {first_message.content}",
            color=ctx.author.color,
        )
        embed.add_field(name="Message", value=f"[Link]({first_message.jump_url})")
        embed.set_author(
            name=first_message.author.name, icon_url=first_message.author.avatar.url
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def roleall(self, ctx: commands.Context, role: disnake.Role):
        await ctx.send("Going to be given everyone the role")
        for member in ctx.guild.members:
            try:
                await member.add_roles(role)
            except:
                await ctx.send(f"Unable to assign role to {member.display_name}")
        await ctx.send(f"Added `{role.name}` to {len(ctx.guild.members)} people")

    @commands.command(hidden=True)
    async def loot(self, ctx: commands.Context, *, message: disnake.Message = None):
        # if ctx.author.id != 432689076626522132:
        #     return await ctx.send("No")

        if not message or message == "^":
            animated = []
            static = []
            async for message in ctx.channel.history(limit=200):
                animated += [
                    (emoji.name, emoji.id)
                    for emoji in message.guild.emojis
                    if emoji.animated
                ]
                static += [
                    (emoji.name, emoji.id)
                    for emoji in message.guild.emojis
                    if not emoji.animated
                ]
        else:
            try:
                message = int(message)
                message = await ctx.channel.fetch_message(message)
            except ValueError:
                message = ctx.message
            finally:
                animated = animated_re.findall(message.content)
                static = static_re.findall(message.content)
        if not static and not animated or not message:
            return await ctx.send("No custom emojis could be found...", delete_after=10)

        loot_lines = []
        for name, id in static:
            loot_lines.append(f" ⚝ {name}: https://cdn.discordapp.com/emojis/{id}.png")
        for name, id in animated:
            loot_lines.append(
                f" ⚝ {name}: https://cdn.discordapp.com/emojis/{id}.gif <animated>"
            )

        max_chars = 2000  # Maximum characters per message
        messages = [
            loot_lines[i : i + max_chars] for i in range(0, len(loot_lines), max_chars)
        ]
        for message_chunk in messages:
            loot_message = "\n".join(message_chunk)
            await ctx.author.send(loot_message)

        total_emojis = len(animated) + len(static)
        await ctx.send(
            f"Check your DMs. You looted {total_emojis} emoji{'s' if total_emojis != 1 else ''}!",
            delete_after=8,
        )
        await ctx.message.delete()


def setup(bot: commands.Bot):
    bot.add_cog(UtilCommands(bot))

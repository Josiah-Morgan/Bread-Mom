import disnake
from disnake.ext import commands

from config import (
    BREAD_KINGDOM_ID,
    BREAD_TEMPLATES_ID,
    CHAT_CHANNEL,
    BREAD_WINNER_B_EMOJI,
    WELCOME_MESSAGE,
    BREAD_KINGDOM_JOIN_ROLES,
    BREAD_TEMPLATES_JOIN_ROLES,
)


class OnJoin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):

        if member.guild.id == BREAD_KINGDOM_ID:
            chat_channel = self.bot.get_channel(CHAT_CHANNEL)
            await chat_channel.send(
                f"{BREAD_WINNER_B_EMOJI} **Hey {member.mention}, Welcome to the server!** {BREAD_WINNER_B_EMOJI}\n\n{WELCOME_MESSAGE}"
            )

            for role in BREAD_KINGDOM_JOIN_ROLES:
                role = disnake.utils.get(member.guild.roles, id=role)
                await member.add_roles(role)

        if member.guild.id == BREAD_TEMPLATES_ID:
            for role in BREAD_TEMPLATES_JOIN_ROLES:
                role = disnake.utils.get(member.guild.roles, id=role)
                await member.add_roles(role)


def setup(bot: commands.Bot):
    bot.add_cog(OnJoin(bot))

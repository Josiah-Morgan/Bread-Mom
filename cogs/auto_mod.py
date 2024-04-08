import disnake
from disnake.ext import commands

from config import WHITE_LISTED, LOG_CHANNEL, BLACK_LISTED_WORDS


class AutoMod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        msg_content = (
            message.content.lower()
            .replace(" ", "")
            .replace("-", "")
            .replace("_", "")
            .replace("+", "")
            .replace("`", "")
            .replace("~", "")
        )

        if message.author.id in WHITE_LISTED or message.author.id == self.bot.user.id:
            return

        log_channel = self.bot.get_channel(LOG_CHANNEL)

        if msg_content in BLACK_LISTED_WORDS:
            await message.delete()
            await message.channel.send(
                f"<@{message.author.id}>, Your not allowed to do that lol"
            )
            msg_content.replace("@everyone", "@ everyone").replace("@here", "@ here")
            await log_channel.send(
                f"**Blacklisted Word**\n\n{message.author.mention}({message.author.id}) has said: {msg_content} in `{message.guild.name}`"
            )


def setup(bot: commands.Bot):
    bot.add_cog(AutoMod(bot))

import disnake
from disnake.ext import commands

from config import SIGNING_VIDEO, COMMON_SIGNING_ERRORS, LINKS_CHANNEL, SUPPORT_CHANNEL

FAQ_DATA = {
    "How to setup signing?": SIGNING_VIDEO,
    "How do I use the signing commands": f"{SIGNING_VIDEO}?t=1m58s",
    "Why won't my signing commands work?": COMMON_SIGNING_ERRORS,
    "How do I invite the bot": f"The link is in the <#{LINKS_CHANNEL}> channel",
    "How do I join the template server": f"The link is in <#{LINKS_CHANNEL}> channel",
    "Why aren't my emojis being made?": "Your server most-likely got rate-limited, **you can test this by trying to add your own emoji, and if it won't let you add it, you got rate-limited**. All you need to do is wait a few hours then try running the command again. \n\n(A good wait to prevent this is by not running too many emoji commands at once)",
    "How do I get my templates, emojis, etc. added to the bot?": "Send anything you think would be a postive additon to the bot to Doggy Soggy",
}


class FAQCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_dropdown(self, inter: disnake.MessageInteraction):
        question = inter.values[0]
        if question in FAQ_DATA:
            answer = FAQ_DATA[question]
            await inter.response.send_message(answer, ephemeral=True)

    @commands.command(hidden=True)
    async def faq_setup(self, ctx: commands.Context):
        await ctx.send(
            components=disnake.ui.StringSelect(
                placeholder="Pick an question to get an answer",
                options=[disnake.SelectOption(label=key) for key in FAQ_DATA.keys()],
                custom_id="FAQ:StringSelect",
            ),
            embed=disnake.Embed(
                title="FAQ Menu",
                description=f"Click on a question below to receive an anwser\n- Note: These are based on common questions and answers. If you have a more specific question or need more assistance, go to the <#{SUPPORT_CHANNEL}> channel",
                color=0xECDEC1,
            ).set_image(url="https://breadwinner.dev/images/cji3fs"),
        )


def setup(bot: commands.Bot):
    bot.add_cog(FAQCommand(bot))

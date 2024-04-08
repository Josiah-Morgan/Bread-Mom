import disnake
from disnake.ext import commands

from config import BREAD_KINGDOM_ID, BREAD_TEMPLATES_ID, LOG_CHANNEL

color = disnake.ButtonStyle.blurple
button_data = {
    BREAD_KINGDOM_ID: [
        {"label": "Updates", "style": color, "emoji": "🤖", "custom_id": "BK:UpdatesButton", "role_id": 758664182643687455},
        {"label": "Announcements", "style": color, "emoji": "📢", "custom_id": "BK:AnnouncementsButton", "role_id": 758664279594369035},
        {"label": "Polls", "style": color, "emoji": "❓", "custom_id": "BK:PollsButton", "role_id": 758664227099246602},
        {"label": "Random", "style": color, "emoji": "💎", "custom_id": "BK:RandomButton", "role_id": 807446922909843506},
    ],
    BREAD_TEMPLATES_ID: [
        {"label": "Template News", "style": color, "emoji": "⚙️", "custom_id": "BT:TemplateNewsButton", "role_id": 844397007531802644},
        {"label": "Announcements", "style": color, "emoji": "📢", "custom_id": "BT:AnnouncementsButton", "role_id": 844397071015870464},
        {"label": "Polls", "style": color, "emoji": "❓", "custom_id": "BT:PollsButton", "role_id": 844397050770096148},
    ],
}

class ButtonRoles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        custom_id = inter.component.custom_id
        guild_button_data = button_data.get(inter.guild.id, [])
        
        for button in guild_button_data:
            if button["custom_id"] == custom_id:
                role = disnake.utils.get(inter.guild.roles, id=button['role_id'])
                break

        try:
          if role in inter.author.roles:
              await inter.author.remove_roles(role)
              await inter.response.send_message(f"The {role.name} has been removed from your roles", ephemeral=True)
          elif role not in inter.author.roles:
              await inter.author.add_roles(role)
              await inter.response.send_message(f"You have been giving the {role.name} role", ephemeral=True)
        except Exception as e:
          log_channel = self.bot.get_channel(LOG_CHANNEL)
          await log_channel.send(e)
      

    @commands.command(hidden=True)
    async def br_setup(self, ctx: commands.Context):
        guild_button_data = button_data.get(ctx.guild.id, [])
        components = [disnake.ui.Button(**{k: v for k, v in button.items() if k != "role_id"}) for button in guild_button_data]

        embed = disnake.Embed(
              title="Role Menu",
              color=0xECDEC1
          )
      
        if ctx.guild.id == BREAD_KINGDOM_ID:
          embed.description="Click the buttons below to gain or remove a role\n\n🤖 **Bot Updates**\nWhen <@730594098695635014> gets an update\n📢 **Annoucements**\nServer updates, bot new, other projects\n❓ **Polls**\nPolls and opinions\n💎 **Random**\nGet pinged for random ||shit|| that I want to tell you"
          embed.set_image(url="https://breadwinner.dev/images/u83nbk")
        elif ctx.guild.id == BREAD_TEMPLATES_ID:
          embed.description = "Click the buttons below to gain or remove a role\n\n⚙ **Template News**\nNew templates, updates, and things related to templates\n📢 **Annoucements**\nServer updates, emojis news, other crap\n❓ **Polls**\nFor polls and opinions"
          embed.set_image(url="https://breadwinner.dev/images/h4kfgo")
        await ctx.send(components=components, embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(ButtonRoles(bot))

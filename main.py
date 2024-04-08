import os

import disnake
from disnake.ext import commands

import keep_alive

intents = disnake.Intents.all()

#intents = disnake.Intents.default()
#intents.message_content = True
#intents.members = True

class BreadMom(commands.Bot):
    def __init__(self):
        super().__init__(intents=intents, activity=disnake.Game(name="over bread"), command_prefix=commands.when_mentioned_or("mom "))
        self.bot = self

    async def start(self, *args, **kwargs):

      for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
          self.bot.load_extension(f'cogs.{filename[:-3]}')
          print(filename + ' Loaded')
  
      await super().start(*args)
  
    async def on_ready(self):
      print('Bot Online')

keep_alive.keep_alive()
bot = BreadMom()
bot.run(os.environ.get("TOKEN"))

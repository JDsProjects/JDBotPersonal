from discord.ext import commands
import discord, random, os

class Buttons(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

async def setup(bot):
  await bot.add_cog(Buttons(bot))
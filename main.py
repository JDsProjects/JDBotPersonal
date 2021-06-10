import discord,  re, os, traceback, logging
from discord.ext import commands
import B, BotConfig

logging.basicConfig(level=logging.INFO)

bot = BotConfig.bot

B.b()
bot.run(os.environ["TOKEN"])
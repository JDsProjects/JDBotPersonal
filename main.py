import contextlib
import logging
import os
import re
import sys
import traceback

import aiohttp
import discord
import dotenv
from discord.ext import commands

from cogs import EXTENSIONS

dotenv.load_dotenv()


async def get_prefix(bot, message):
    extras = ["jd+", "jd+", "jd+"]
    comp = re.compile("^(" + "|".join(map(re.escape, extras)) + ").*", flags=re.I)
    match = comp.match(message.content)
    if match is not None:
        extras.append(match.group(1))
    return commands.when_mentioned_or(*extras)(bot, message)


class JDBotPersonal(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.special_access = {}

    async def start(self, *args, **kwargs):
        self.session = aiohttp.ClientSession()
        await super().start(*args, **kwargs)

    async def close(self):
        await self.session.close()
        await super().close()

    async def getch_member(self, guild, member_id):
        member = None
        with contextlib.suppress(discord.Forbidden, discord.HTTPException):
            member = guild.get_member(member_id) or await guild.fetch_member(member_id)
        return member

    async def getch_user(self, user_id):
        user = None

        with contextlib.suppress(discord.NotFound, discord.HTTPException):
            user = self.get_user(user_id) or await self.fetch_user(user_id)
        return user

    async def setup_hook(self):
        await bot.load_extension("jishaku")

        for cog in EXTENSIONS:
            try:
                await self.load_extension(f"{cog}")
            except commands.errors.ExtensionError:
                traceback.print_exc()


bot = JDBotPersonal(command_prefix=(get_prefix), intents=discord.Intents.all(), strip_after_prefix=True)


@bot.event
async def on_error(event, *args, **kwargs):
    more_information = sys.exc_info()
    error_wanted = traceback.format_exc()
    traceback.print_exc()
    # print(more_information[0])


logging.basicConfig(level=logging.INFO)


bot.run(os.environ["TOKEN"])

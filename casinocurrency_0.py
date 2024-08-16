import discord
import json
from discord.ext import commands


class Casinocurrency_0(commands.Cog):
    def __init__(self, client):
        self.client = client

async def setup(client):
    await client.add_cog(Casinocurrency_0(client))
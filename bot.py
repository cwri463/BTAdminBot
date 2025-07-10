import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

# Load command modules from ./cogs
@bot.event
async def setup_hook():
    await bot.load_extension("cogs.tasks")  # Load tasks feature

bot.run(TOKEN)

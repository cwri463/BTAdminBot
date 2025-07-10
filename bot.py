import os
import discord

# Read token and guild from environment variables
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("DISCORD_GUILD_ID")  # Add this in Railway as a variable

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        # Sync only to your server (faster than global)
        guild = discord.Object(id=int(GUILD_ID))
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        print(f"Synced commands to guild {GUILD_ID}")

client = MyClient()

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user} (ID: {client.user.id})")

# Define the slash command
@client.tree.command(name="claim", description="Submit a task for clan XP")
async def claim(interaction: discord.Interaction, task_name: str):
    await interaction.response.send_message(
        f"📝 {interaction.user.mention} claimed task: `{task_name}`!", ephemeral=True
    )

client.run(TOKEN)

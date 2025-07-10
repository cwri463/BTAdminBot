import os
import discord

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))
GUEST_ROLE_ID = int(os.getenv("GUEST_ROLE_ID"))
MEMBER_ROLE_ID = int(os.getenv("MEMBER_ROLE_ID"))
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True
intents.reactions = True

class BTAdminBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)
        self.tracked_joins = {}  # Track messages to users

    async def setup_hook(self):
        await self.tree.sync(guild=discord.Object(id=GUILD_ID))

client = BTAdminBot()

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user} (ID: {client.user.id})")

@client.event
async def on_member_join(member):
    guild = client.get_guild(GUILD_ID)
    guest_role = guild.get_role(GUEST_ROLE_ID)
    log_channel = guild.get_channel(LOG_CHANNEL_ID)

    await member.add_roles(guest_role, reason="Auto-assigned Guest role")

    if log_channel:
        msg = await log_channel.send(
            f"👤 **{member.mention}** joined the server.\n"
            "React with ✅ to promote to **Member**, or ❌ to leave as **Guest**."
        )
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        # Store mapping of message ID to user
        client.tracked_joins[msg.id] = member.id

@client.event
async def on_raw_reaction_add(payload):
    # Ignore bot reactions
    if payload.user_id == client.user.id:
        return

    # Only process reactions in the join log channel
    if payload.channel_id != LOG_CHANNEL_ID:
        return

    # Only process ✅ or ❌
    if payload.emoji.name not in ["✅", "❌"]:
        return

    message_id = payload.message_id
    member_id = client.tracked_joins.get(message_id)

    if not member_id:
        return  # Not a tracked join message

    guild = client.get_guild(GUILD_ID)
    member = guild.get_member(member_id)
    mod = guild.get_member(payload.user_id)
    log_channel = guild.get_channel(LOG_CHANNEL_ID)

    if payload.emoji.name == "✅":
        await member.remove_roles(guild.get_role(GUEST_ROLE_ID), reason="Promoted by mod reaction")
        await member.add_roles(guild.get_role(MEMBER_ROLE_ID), reason="Approved by mod")

        if log_channel:
            await log_channel.send(f"✅ {mod.mention} promoted {member.mention} to **Member**.")

    elif payload.emoji.name == "❌":
        if log_channel:
            await log_channel.send(f"❌ {mod.mention} chose to leave {member.mention} as **Guest**.")

client.run(TOKEN)

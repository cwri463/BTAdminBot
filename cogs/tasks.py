import discord
from discord.ext import commands

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="claim", description="Submit a task for clan XP")
    async def claim(self, ctx: discord.ApplicationContext, task_name: str):
        await ctx.respond(f"📝 {ctx.author.mention} claimed task: `{task_name}`! (Proof pending review)")

def setup(bot):
    bot.add_cog(Tasks(bot))

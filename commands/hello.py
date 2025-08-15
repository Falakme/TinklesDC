from discord import app_commands, Interaction
from discord.ext.commands import Bot

def setup(bot: Bot):
    @bot.tree.command(name="hello", description="Say hello!")
    async def hello(interaction: Interaction):
        await interaction.response.send_message(f"Hello, {interaction.user.mention}!")

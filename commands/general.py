from discord import app_commands, Interaction
from discord.ext.commands import Bot

# /poll [question] – Create a poll (anyone)
def setup(bot: Bot):

# /feedback [message] – Send feedback to admins (anyone)
    @bot.tree.command(name="feedback", description="Send feedback to admins.")
    @app_commands.describe(message="Your feedback message")
    async def feedback(interaction: Interaction, message: str):
        import os
        admin_channel_id = int(os.getenv('ADMIN_CHANNEL_ID', '0'))
        channel = interaction.client.get_channel(admin_channel_id)
        if channel:
            await channel.send(f"Feedback from {interaction.user.mention}: {message}")
            await interaction.response.send_message("Thank you for your feedback!", ephemeral=True)
        else:
            await interaction.response.send_message("Admin channel not found.", ephemeral=True)

# /clubinfo – About the club (anyone)
    @bot.tree.command(name="clubinfo", description="About the club.")
    async def clubinfo(interaction: Interaction):
        await interaction.response.send_message("The Falak Club is a High School coding club under Falak.me and associated with The Hack Foundation")

# /mentors – List mentors (anyone)
    @bot.tree.command(name="mentors", description="List mentors.")
    async def mentors(interaction: Interaction):
        await interaction.response.send_message("Mentors: (pending)")


import discord
from discord import app_commands, Interaction
from discord.ext.commands import Bot
from discord import Permissions
from discord.ext import commands

# Helper: Check if user is admin or mod
def is_admin_or_mod(interaction: Interaction):
    perms = interaction.user.guild_permissions
    return perms.administrator or perms.manage_guild or perms.manage_channels

# /lock – Lock a channel (admin/mod)
def setup(bot: Bot):
    @bot.tree.command(name="lock", description="Lock the current channel.")
    async def lock(interaction: Interaction):
        if not is_admin_or_mod(interaction):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = False
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message("Channel locked.")

# /unlock – Unlock a channel (admin/mod)
    @bot.tree.command(name="unlock", description="Unlock the current channel.")
    async def unlock(interaction: Interaction):
        if not is_admin_or_mod(interaction):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = True
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message("Channel unlocked.")

# /announce [message] – Send club announcements (admin/mod)
    @bot.tree.command(name="announce", description="Announce a previously sent message in a specific channel.")
    @app_commands.describe(message_id="ID of the message to announce", channel="Channel to send the announcement in")
    async def announce(interaction: Interaction, message_id: str, channel: discord.TextChannel):
        if not is_admin_or_mod(interaction):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return
        try:
            msg = await channel.fetch_message(int(message_id))
            await channel.send(f"{msg.content}")
            await interaction.response.send_message(f"Announcement sent in {channel.mention}!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)

# /pingall – Ping all members (admin/mod)

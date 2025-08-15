@bot.tree.command(name="purge", description="Delete n messages in this channel (admin only)")
@app_commands.describe(amount="Number of messages to delete")
async def purge(interaction: Interaction, amount: int):
        try:
            if not is_admin(interaction):
                await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
                return
            deleted = await interaction.channel.purge(limit=amount)
            await interaction.response.send_message(f"Deleted {len(deleted)} messages.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)

import discord
from discord import app_commands, Interaction
from discord.ext.commands import Bot

# Helper: Check if user is admin
def is_admin(interaction: Interaction):
    return interaction.user.guild_permissions.administrator

# /status [text] – Set bot status (admin only)
def setup(bot: Bot):


    @bot.tree.command(name="status", description="Set the bot's status. Usage: /status type:[playing|watching|listening] text:[your text] rotate:[true|false]")
    @app_commands.describe(type="Type: playing, watching, listening", text="The status text", rotate="Add to rotation (true/false)")
    async def status(interaction: Interaction, type: str, text: str, rotate: bool = False):
        allowed_types = {
            "playing": lambda n: discord.Game(name=n),
            "watching": lambda n: discord.Activity(type=discord.ActivityType.watching, name=n),
            "listening": lambda n: discord.Activity(type=discord.ActivityType.listening, name=n)
        }
        if not is_admin(interaction):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return
        if type.lower() not in allowed_types:
            await interaction.response.send_message("Invalid type. Use one of: playing, watching, listening.", ephemeral=True)
            return
        if rotate:
            # Save to rotation file
            import json
            statuses = []
            try:
                with open("status_rotation.json", "r") as f:
                    statuses = json.load(f)
            except Exception:
                pass
            statuses.append({"text": text, "type": type.lower()})
            with open("status_rotation.json", "w") as f:
                json.dump(statuses, f)
            await interaction.response.send_message(f"Added to status rotation: {type.title()} {text}")
        else:
            activity = allowed_types[type.lower()](text)
            await interaction.client.change_presence(activity=activity)
            await interaction.response.send_message(f"Status set to: {type.title()} {text}")

    import asyncio
    async def rotate_statuses(bot):
        import json
        allowed_types = {
            "playing": lambda n: discord.Game(name=n),
            "watching": lambda n: discord.Activity(type=discord.ActivityType.watching, name=n),
            "listening": lambda n: discord.Activity(type=discord.ActivityType.listening, name=n)
        }
        while True:
            try:
                with open("status_rotation.json", "r") as f:
                    statuses = json.load(f)
                for s in statuses:
                    activity_type = s.get("type", "playing")
                    text = s.get("text", "")
                    if activity_type.lower() in allowed_types:
                        activity = allowed_types[activity_type.lower()](text)
                        await bot.change_presence(activity=activity)
                        await asyncio.sleep(30)
            except Exception:
                await asyncio.sleep(30)

    # Start rotation task on bot ready
    @bot.event
    async def on_ready():
        if not hasattr(bot, "_status_rotation_started"):
            bot._status_rotation_started = True
            bot.loop.create_task(rotate_statuses(bot))

# /restart – Restart the bot (admin only)
    @bot.tree.command(name="restart", description="Restart the bot.")
    async def restart(interaction: Interaction):
        # Only allow users with the specific role
        allowed_role_id = 1405898511186133152
        if not any(role.id == allowed_role_id for role in interaction.user.roles):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return
        await interaction.response.send_message("Restarting bot...", ephemeral=True)
        import os, sys
        os.execv(sys.executable, ['python'] + sys.argv)

# /uptime – Bot uptime (admin/mod)
    import time
    bot_start_time = time.time()
    @bot.tree.command(name="uptime", description="Show bot uptime.")
    async def uptime(interaction: Interaction):
        if not is_admin(interaction):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return
        now = time.time()
        uptime_seconds = int(now - bot_start_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await interaction.response.send_message(f"Uptime: {hours}h {minutes}m {seconds}s")

import discord
from discord import app_commands, Interaction
from discord.ext.commands import Bot
import json
import os

todo_file = 'todo_data.json'

def load_todos():
    if os.path.exists(todo_file):
        with open(todo_file, 'r') as f:
            return json.load(f)
    return {}

def save_todos(todos):
    with open(todo_file, 'w') as f:
        json.dump(todos, f)

def setup(bot: Bot):
    @bot.tree.command(name="todo", description="Show or update your personal to-do list.")
    @app_commands.describe(action="add/remove/show", item="Item to add/remove")
    async def todo(interaction: Interaction, action: str, item: str = None):
        user_id = str(interaction.user.id)
        todos = load_todos()
        if action == "add" and item:
            todos.setdefault(user_id, []).append(item)
            save_todos(todos)
            await interaction.response.send_message(f"Added to your to-do list: {item}", ephemeral=True)
        elif action == "remove" and item:
            if user_id in todos and item in todos[user_id]:
                todos[user_id].remove(item)
                save_todos(todos)
                await interaction.response.send_message(f"Removed from your to-do list: {item}", ephemeral=True)
            else:
                await interaction.response.send_message("Item not found in your to-do list.", ephemeral=True)
        elif action == "show":
            items = todos.get(user_id, [])
            if items:
                await interaction.response.send_message("Your to-do list:\n" + "\n".join(f"- {i}" for i in items), ephemeral=True)
            else:
                await interaction.response.send_message("Your to-do list is empty!", ephemeral=True)
        else:
            await interaction.response.send_message("Usage: /todo action:[add|remove|show] item:[item text]", ephemeral=True)

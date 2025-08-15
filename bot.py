import aiohttp
import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import importlib
import pathlib

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

CDN_CHANNEL_ID = 1405954610325356726

@bot.event
async def on_message(message):
    print(f"on_message: channel={message.channel.id}, attachments={len(message.attachments) if hasattr(message, 'attachments') else 'N/A'}, author.bot={message.author.bot}")
    # Only process messages in the cdn channel and skip bot messages
    if message.channel.id == CDN_CHANNEL_ID and not message.author.bot:
        # If message has attachments, handle CDN upload
        if message.attachments:
            file_urls = [a.url for a in message.attachments]
            print(f"CDN upload triggered. File URLs: {file_urls}")
            api_url = 'https://cdn.hackclub.com/api/v3/new'
            headers = {
                'Authorization': 'Bearer beans',
                'Content-Type': 'application/json'
            }
            max_retries = 3
            for attempt in range(1, max_retries + 1):
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.post(api_url, headers=headers, json=file_urls) as resp:
                            print(f"CDN API response status: {resp.status}")
                            resp_text = await resp.text()
                            print(f"CDN API response data: {resp_text}")
                            if resp.status == 200:
                                data = await resp.json()
                                deployed_urls = [f["deployedUrl"] for f in data.get("files", [])]
                                deployed_urls_str = '\n'.join(deployed_urls)
                                await message.reply(f"Uploaded to CDN: {deployed_urls_str}")
                                break
                            else:
                                await message.reply(f"CDN upload failed: {resp.status}")
                                break
                except Exception as e:
                    print(f"CDN upload attempt {attempt} failed: {e}")
                    if attempt == max_retries:
                        await message.reply(f"CDN upload failed after {max_retries} attempts: {e}")
                    else:
                        import asyncio
                        await asyncio.sleep(2 * attempt)
        # If message is a link, allow it
        elif message.content and (message.content.startswith('http://') or message.content.startswith('https://')):
            pass
        # Otherwise, delete the message
        else:
            try:
                await message.delete()
                print(f"Deleted non-attachment, non-link message in CDN channel from {message.author}")
            except Exception as e:
                print(f"Failed to delete message: {e}")
    await bot.process_commands(message)
def load_commands():
    commands_path = pathlib.Path(__file__).parent / 'commands'
    for file in commands_path.glob('*.py'):
        if file.name.startswith('_') or not file.name.endswith('.py'):
            continue
        module_name = f'commands.{file.stem}'
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, 'setup'):
                module.setup(bot)
        except Exception as e:
            print(f"Failed to load command module {module_name}: {e}")
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} slash commands.')
    except Exception as e:
        print(f'Error syncing commands: {e}')

load_commands()
bot.run(TOKEN)

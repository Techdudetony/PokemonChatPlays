from twitchio.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

print("Loaded env:")
print("Token:", os.getenv("TWITCH_TOKEN"))
print("Nick:", os.getenv("TWITCH_NICK"))
print("Channel:", os.getenv("TWITCH_CHANNEL"))

bot = commands.Bot(
    token=os.getenv("TWITCH_TOKEN"),
    prefix="!",
    initial_channels=[os.getenv("TWITCH_CHANNEL")]
)

@bot.event
async def event_Ready():
    print(f"✅ Connected as {os.getenv('TWITCH_NICK')}")

@bot.event
async def event_message(message):
    print(f"{message.author.name}: {message.content}")
    await bot.handle_commands(message)

@bot.command(name='up')
async def up(ctx):
    print("Received !up")
    #TODO: Add to queue or  call Lua bridge here

bot.run()
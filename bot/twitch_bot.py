from bot.command_queue import CommandQueue
from controller.input_handler import handle_input
from twitchio.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

command_queue = CommandQueue()

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
async def event_ready():
    print(f"✅ Connected as {os.getenv('TWITCH_NICK')}")
    bot.loop.create_task(command_queue.start(handle_input))  


@bot.event
async def event_message(message):
    print(f"{message.author.name}: {message.content}")

    # Only respond to messages starting with "!"
    if not message.content.startswith("!"):
        return
    
    full_cmd = message.content[1:].lower() # Remove "!" and lowercase
    base_cmd = ''.join(filter(str.isalpha, full_cmd)) # Extract the letters (e.g. "up" from "up4")
    count_str = ''.join(filter(str.isdigit, full_cmd)) # Extract the number (e.g. "4" from "up4")

    count = int(count_str) if count_str else 1
    count = min(count, 10) # Limit to 10 max

    message.command_name = base_cmd
    message.command_count = count

    await bot.handle_commands(message)

commands_map = {
    "up": "Moving up",
    "down": "Moving down",
    "left": "Moving left",
    "right": "Moving right",
    "a": "Pressing A",
    "b": "Pressing B",
    "start": "Pressing Start",
    "select": "Pressing Select"
}

for cmd, response in commands_map.items():
    @bot.command(name=cmd)
    async def command_template(ctx, resp=response, cmd_name=cmd):
        count = getattr(ctx.message, 'command_count', 1)
        for i in range(count):
            print(f"Executing {cmd_name} ({i+1}/{count})")
            # TODO: Trigger Lua logic here per step

bot.run()
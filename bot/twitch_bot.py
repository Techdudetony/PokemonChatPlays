from bot.command_queue import CommandQueue
from controller.input_handler import handle_input
from twitchio.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

command_queue = CommandQueue()

def append_to_input_file(command_str):
    with open("controller/input.txt", "a") as f:
        f.write(f"{command_str}\n")
        
def create_command_handler(cmd_name, response):
    @commands.command(name=cmd_name)
    async def command_template(ctx):
        count = getattr(ctx.message, 'command_count', 1)
        for i in range(count):
            print(f"Executing {cmd_name} ({i+1}/{count})")
            append_to_input_file(f"!{cmd_name}{count}")
    bot.add_command(command_template)

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
    
    if message.content.startswith("!"):
        full_cmd = message.content[1:].lower() # Remove "!" and lowercase
        base = ''.join(filter(str.isalpha, full_cmd)) # Extract the letters (e.g. "up" from "up4")
        digits = ''.join(filter(str.isdigit, full_cmd)) # Extract the number (e.g. "4" from "up4")
        count = min(int(digits) if digits else 1, 10)
        
        command_str = f"!{base}{count}"
        append_to_input_file(command_str)

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
    create_command_handler(cmd, response)

bot.run()
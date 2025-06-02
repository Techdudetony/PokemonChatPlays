from bot.command_queue import CommandQueue
from bot.cooldown_manager import CooldownManager
from bot.chat_rate_monitor import ChatRateMonitor
from controller.input_handler import handle_input
from twitchio.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

SPAM_THRESHOLD = int(os.getenv("SPAM_THRESHOLD", 12))
SLOWMODE_DISABLE_THRESHOLD = int(os.getenv("SLOWMODE_DISABLE_THRESHOLD", 6))
CHAT_WINDOW_SIZE = int(os.getenv("CHAT_WINDOW_SIZE", 10))
CHAT_COOLDOWN_PERIOD = int(os.getenv("CHAT_COOLDOWN_PERIOD", 5))

command_queue = CommandQueue()
cooldowns = CooldownManager(cooldown_seconds=2)
chat_monitor = ChatRateMonitor(window_size=CHAT_WINDOW_SIZE, cooldown_period=CHAT_COOLDOWN_PERIOD)

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
    
    chat_monitor.log_message(username=message.author.name)

    # Auto Slow Mode ON
    if chat_monitor.is_spammy(threshold=SPAM_THRESHOLD):
        print("🚨 Spam detected! Enabling Slow Mode.")
        await message.channel.slowmode_delay(5)

    # Auto Slow Mode OFF
    elif chat_monitor.should_disable_slowmode(disable_threshold=SLOWMODE_DISABLE_THRESHOLD):
        print("✅ Spam has settled. Disabling Slow Mode.")
        await message.channel.slowmode_delay(0)

    if not message.content.startswith("!"):
        return

    # Per-user cooldown check
    if cooldowns.is_on_cooldown(message.author.name):
        print(f"⏳ {message.author.name} is on cooldown.")
        return

    cooldowns.update_timestamp(message.author.name)

    if command_queue.size() >= 100:
        print(f"🚫 Queue is full. Command from {message.author.name} was ignored.")
        return

    full_cmd = message.content[1:].lower()
    base = ''.join(filter(str.isalpha, full_cmd))
    digits = ''.join(filter(str.isdigit, full_cmd))
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
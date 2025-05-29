import datetime

async def handle_input(command_name):
    print(f"[InputHandler] Sending command to emulator: {command_name}")

    with open("controller/input.txt", "a") as f:
        f.write(f"{datetime.datetime.now().isoformat()} {command_name}\n")

    # You could also trigger a Lua socket or modify memory here instead

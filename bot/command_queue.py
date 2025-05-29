import asyncio

class CommandQueue:
    def __init__(self, delay=0.5):
        self.queue = asyncio.Queue()
        self.delay = delay
        self.is_running = False

    async def start(self, handle_function):
        if self.is_running:
            return
        self.is_running = True

        while True:
            command_name, count = await self.queue.get()
            for i in range(count):
                print(f"[Queue] Processing {command_name} ({i + 1}/{count})")
                await handle_function(command_name)
                await asyncio.sleep(self.delay)
            self.queue.task_done()
    
    async def add_command(self, command_name, count):
        await self.queue.put((command_name, count))
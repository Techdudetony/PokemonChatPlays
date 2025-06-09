import asyncio

class CommandQueue:
    def __init__(self, delay=3.0, max_size=50):
        self.queue = asyncio.Queue(maxsize=max_size)
        self.delay = delay
        self.is_running = False

    async def start(self, handle_function):
        if self.is_running:
            return
        self.is_running = True

        while True:
            command_name, count = await self.queue.get()
            await asyncio.sleep(self.delay)
            for i in range(count):
                print(f"[Queue] Processing {command_name} ({i + 1}/{count})")
                await handle_function(command_name)
                await asyncio.sleep(self.delay)
            self.queue.task_done()
    
    async def add_command(self, command_name, count):
        await self.queue.put((command_name, count))
        
    def size(self):
        return self.queue.qsize()

    def is_full(self):
        return self.queue.full()
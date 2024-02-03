import os
import time
import asyncio
from threading import Thread
from pynput.keyboard import Controller as KeyboardController, KeyCode, Listener, Key
from pynput.mouse import Controller as MouseController

class ScrollingMacro:
    def __init__(self, delay_ms, key_bind, mode):
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        self.is_running = False
        self.delay_ms = delay_ms
        self.key_bind = key_bind
        self.mode = mode

    def toggle(self):
        self.is_running = not self.is_running
        if self.is_running:
            macro_thread = Thread(target=self.run_macro)
            macro_thread.start()

    async def execute_macro(self):
        if self.mode == "firstperson":
            await self.scroll_up_and_down()
        elif self.mode == "thirdperson":
            await self.press_i_and_o()

    async def scroll_up_and_down(self):
        while self.is_running:
            self.mouse.scroll(0, 1)
            await asyncio.sleep(self.delay_ms / 1000.0)
            self.mouse.scroll(0, -1)
            await asyncio.sleep(self.delay_ms / 1000.0)

    async def press_i_and_o(self):
        while self.is_running:
            self.keyboard.press('i')
            await asyncio.sleep(self.delay_ms / 1000.0)
            self.keyboard.release('i')
            await asyncio.sleep(self.delay_ms / 1000.0)
            
            self.keyboard.press('o')
            await asyncio.sleep(self.delay_ms / 1000.0)
            self.keyboard.release('o')
            await asyncio.sleep(self.delay_ms / 1000.0)

    def run_macro(self):
        asyncio.run(self.execute_macro())

def on_key_press(key):
    if key == key_bind:
        scrolling_macro.toggle()

if __name__ == "__main__":
    config_file = os.path.join(os.path.dirname(__file__), "config.txt")

    with open(config_file, "r") as file:
        config_data = file.read()

    delay_start = config_data.find("delay = ") + len("delay = ")
    delay_end = config_data.find("\n", delay_start)
    delay_ms = int(config_data[delay_start:delay_end])

    mode_start = config_data.find("mode = ") + len("mode = ")
    mode_end = config_data.find("\n", mode_start)
    mode = config_data[mode_start:mode_end]

    key_start = config_data.find("key = ") + len("key = ")
    key_end = config_data.find("]", key_start)
    key_bind = KeyCode.from_char(config_data[key_start:key_end].strip())

    scrolling_macro = ScrollingMacro(delay_ms, key_bind, mode)

    listener = Listener(on_press=on_key_press)
    listener.start()

    print("VIOLENTS DAHOOD MACRO discord:violentqm (Press {} to toggle)...".format(config_data[key_start:key_end].strip().upper()))

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        listener.stop()
        print("Macro stopped by user.")

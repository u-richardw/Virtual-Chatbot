import os
import twitchio
from twitchio.ext import commands
from memory import load_memory, save_memory
from ai_handler import get_ai_response


TWITCH_TOKEN = "oauth:1ashkq252nievdfihwpy491chkqmj2"

TWITCH_CHANNEL = "schrodingerlee"
BOT_NICKNAME = "tai_chan_bot"

class TaiChanBot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=TWITCH_TOKEN,
            prefix="!",
            nick=BOT_NICKNAME,
            initial_channels=[TWITCH_CHANNEL]
        )
        self.memory = load_memory()  # Initialize memory

    async def event_ready(self):
        print(f"{BOT_NICKNAME} is now connected to Twitch chat!")

    async def event_message(self, message):
        if message.echo:
            return  # Ignore bot's own messages
        
        chat_text = message.content.strip()
        username = message.author.name
        print(f"[Twitch] {username}: {chat_text}")

        # Ignore spammy messages or short reactions
        if len(chat_text) < 5 or chat_text.startswith("!") or chat_text.lower() in ["lol", "lmao", "xd"]:
            return

        # Prioritize meaningful messages
        if "tai-chan" in chat_text.lower() or any(c.isdigit() for c in chat_text):
            self.memory.insert(0, f"{username}: {chat_text}")  # Prioritize
        else:
            self.memory.append(f"{username}: {chat_text}")

        # Keep memory size manageable
        if len(self.memory) > 50:
            self.memory.pop()

        save_memory(self.memory)  # Save memory

        # Respond if Tai-Chan is mentioned
        if "tai-chan" in chat_text.lower():
            response = get_ai_response(chat_text, self.memory)
            await message.channel.send(f"@{username} {response}")  # Mention user for better engagement

# Run the bot
if __name__ == "__main__":
    bot = TaiChanBot()
    bot.run()

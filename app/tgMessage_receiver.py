from telethon import TelegramClient, events
from telethon.errors.rpcerrorlist import AuthKeyError
from telethon.sync import TelegramClient as SyncTelegramClient
import config
import time
import pickle
import json


try:
    client = TelegramClient(config.session_name, config.api_id, config.api_hash, timeout=60)
    client.start()
except AuthKeyError:
    client = SyncTelegramClient(config.session_name, config.api_id, config.api_hash, timeout=60)
    client.start()
if client:
    config.logging.info("client start")
with open("group_ids.json", 'r') as f:
    chat_names = json.load(f, object_hook=config.custom_decoder)


@client.on(events.NewMessage(chats=list(chat_names.keys()), incoming=True))
async def handle_new_message(event):
    sender = await event.get_sender()
    if not sender or not hasattr(sender, 'bot') or sender.bot:
        return
    message_text = event.message.message
    chat = await event.get_chat()
    sender_id = str(sender.id)
    sender_name = str(sender.first_name) + ' ' + str(sender.last_name)
    sender_username = str(sender.username)
    for keyword in config.keywords:
        if len(message_text) > 10:
            return
        if keyword in message_text:
            title = -1000000000000 - chat.id
            data = {"keyword": keyword, "username": sender_username, "sender_name": sender_name, "sender_id": sender_id,
                    "title": chat_names[title],
                    "message_text": message_text, "datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
            config.logging.info(json.dumps(data))
            try:
                if config.auto_send:
                    await client.send_message(sender, config.message)
                    config.logging.info(sender_name + "   send success")
                    config.save_message(sender_id, sender_name, sender_username, chat_names[title], message_text, 'success',
                                          pickle.dumps(sender))
                else:
                    config.save_message(sender_id, sender_name, sender_username, chat_names[title], message_text,
                                        'error',
                                        pickle.dumps(sender))
            except Exception as e:
                config.logging.exception(e)
                config.logging.error(sender_name + "   send faild")
                config.save_message(sender_id, sender_name, sender_username, chat_names[title], message_text, 'error',
                                          pickle.dumps(sender))
            return


config.logging.info(f"Listening for messages containing {config.keywords} in chats {chat_names}...")
client.run_until_disconnected()

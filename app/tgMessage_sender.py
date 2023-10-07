import os

from telethon import TelegramClient
from telethon.errors.rpcerrorlist import AuthKeyError
from telethon.sync import TelegramClient as SyncTelegramClient
import config
import pickle


def resend_message(id):
    os.system(f"cp {config.session_name}.session {config.session_name}_new.session")
    try:
        client = TelegramClient(f"{config.session_name}_new", config.api_id, config.api_hash, timeout=60)
        client.start()
    except AuthKeyError:
        client = SyncTelegramClient(f"{config.session_name}_new", config.api_id, config.api_hash, timeout=60)
        client.start()
    sender = config.get_sender(id)
    if not sender:
        return False
    try:
        sender = pickle.loads(sender)
        client.send_message(sender, config.message)
        config.update_message(id, 'success')
        return True
    except Exception as e:
        config.logging.error("resend message error")
        config.logging.exception(e)
        config.update_message(id, 'error')
    finally:
        client.disconnect()
        os.system(f"rm -f {config.session_name}_new.session")
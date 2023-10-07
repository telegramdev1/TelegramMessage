from telethon import TelegramClient
import json
import config
group_ids = {}


async def main():
    # 创建 Telethon 客户端对象并进行身份验证
    client = TelegramClient(config.session_name, config.api_id, config.api_hash, timeout=60)
    await client.start()

    # 获取所有群组的 ID 和名称
    dialogs = await client.get_dialogs()
    groups = [dialog for dialog in dialogs if dialog.is_group]
    for group in groups:
        print(f"Group ID: {group.id}, Group Name: {group.title}")
        if group.entity.username:
            group_ids[group.id] = group.entity.username
        else:
            group_ids[group.id] = group.entity.usernames[0].username
    with open("group_ids.json", 'w') as f:
        json.dump(group_ids, f, separators=(',', ':'))
    # 断开连接
    await client.disconnect()


if __name__ == "__main__":
    # 运行主循环
    import asyncio
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except Exception as e:
        print(f"An error occurred: {e}")

import asyncio
from redis_client import redis_client
from websocket_manager import manager

STREAM = "chat-stream"
GROUP = "chat-group"
CONSUMER = "chat-consumer-1"

async def setup_group():
    try:
        await redis_client.xgroup_create(
            STREAM, GROUP, id="0", mkstream=True
        )
    except Exception:
        pass

async def consume_messages():
    await setup_group()

    while True:
        result = await redis_client.xreadgroup(
            groupname=GROUP,
            consumername=CONSUMER,
            streams={STREAM: ">"},
            count=10,
            block=5000
        )

        for _, messages in result:
            for msg_id, data in messages:
                receiver_id = data["receiver_id"]

                await manager.send_to_user(receiver_id, data)

                await redis_client.xack(STREAM, GROUP, msg_id)

        await asyncio.sleep(0)

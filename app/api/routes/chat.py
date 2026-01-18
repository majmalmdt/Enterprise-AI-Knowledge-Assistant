from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from app.services.rag_service import RAGService
from app.core.redis import redis
router = APIRouter()

rag_service = RAGService(top_k=5)
channel = "chat_events"

@router.websocket("/ws/chat/{section_id}")
async def websocket_endpoint(websocket: WebSocket, section_id: str):
    await websocket.accept()

    pubsub = redis.pubsub()
    await pubsub.subscribe(channel)

    async def send_worker_messages():
        try:
            async for message in pubsub.listen():
                if message is None or message["type"] != "message":
                    continue
                data = message["data"]
                await websocket.send_text(data)
        except Exception as e:
            print("❌ Redis listener error:", e)

    send_task = asyncio.create_task(send_worker_messages())

    try:
        while True:
            data = await websocket.receive_text()

            response = rag_service.answer_question(data, section_id)

            await redis.publish(channel, response["answer"])

    except WebSocketDisconnect:
        send_task.cancel()
        await pubsub.unsubscribe(channel)
        await websocket.close()

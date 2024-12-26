from bson import ObjectId
from fastapi import FastAPI, WebSocket, HTTPException, status, WebSocketDisconnect, Response
from fastapi.encoders import ENCODERS_BY_TYPE
import asyncio
import random

import schema
from database import messages
from models import Message

ENCODERS_BY_TYPE[ObjectId] = str
app = FastAPI()


@app.get("/api/messages/{id}", response_model=schema.Message)
async def get_message(id: str):
    message_in_db = await Message.find_by_id(id)
    if not message_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such message")
    return {**message_in_db}


@app.get("/api/messages", response_model=list[schema.Message])
async def get_messages(from_user_id: int | None = None, to_user_id: int | None = None):
    return await Message.find_all(from_user_id, to_user_id)


@app.post("/api/messages", status_code=status.HTTP_201_CREATED)
async def create_message(message: schema.MessageIn):
    new_message = await Message.create(message)
    if not new_message:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No such message")
    return {**new_message}


@app.put("/api/messages/{id}")
async def update_message(id: str, updated_message: schema.MessageIn):
    message_in_db = await Message.find_by_id(id)
    if not message_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await Message.update(id, updated_message.model_dump())
    return {"id": id}


@app.delete("/api/messages/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(id: str):
    result = await Message.delete(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return Response(content="Successfully deleted")


@app.websocket("/api/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            count = await messages.count_documents({})
            if count == 0:
                await websocket.send_text("No messages in the database.")
            else:
                random_index = random.randint(0, count - 1)
                random_message = await messages.find().skip(random_index).limit(1).to_list(1)
                if random_message:
                    random_message = random_message[0]
                    del random_message["_id"]
                    random_message["publish_timestamp"] = random_message["publish_timestamp"].isoformat()
                    await websocket.send_json(random_message)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("WebSocket disconnected")

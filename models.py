from bson import ObjectId

import utils
from schema import MessageIn
from database import messages


class Message:
    @staticmethod
    async def create(message: MessageIn) -> dict | None:
        unix_time = utils.get_unix_time()
        message_dict = {
            "publish_timestamp": unix_time,
            "id": str(ObjectId()),
            **message.model_dump()
        }
        inserted = await messages.insert_one(message_dict)
        new_item = await messages.find_one({"_id": inserted.inserted_id})
        return new_item

    @staticmethod
    async def find_by_id(message_id: str) -> dict | None:
        return await messages.find_one({"id": message_id})

    @staticmethod
    async def find_all(from_user_id: int | None = None, to_user_id: int | None = None) -> list:
        if from_user_id is not None and to_user_id is not None:
            query = messages.find({
                "from_user_id": from_user_id,
                "to_user_id": to_user_id
            })
        elif from_user_id is not None:
            query = messages.find({
                "from_user_id": from_user_id,
            })
        elif to_user_id is not None:
            query = messages.find({
                "to_user_id": to_user_id
            })
        else:
            query = messages.find()
        return await query.sort("publish_timestamp", -1).to_list()

    @staticmethod
    async def update(message_id: str, data: dict) -> dict | None:
        unix_time = utils.get_unix_time()
        result = await messages.update_one(
            {"id": message_id}, {"$set": {"edit_timestamp": unix_time, **data}}
        )
        if result.modified_count > 0:
            return await messages.find_one({"id": message_id})
        return None

    @staticmethod
    async def delete(message_id: str) -> bool:
        result = await messages.delete_one({"id": message_id})
        return result.deleted_count > 0

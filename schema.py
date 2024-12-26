from pydantic import BaseModel
from datetime import datetime


class MessageIn(BaseModel):
    content: str
    from_user_id: int
    to_user_id: int


class MessageOut(BaseModel):
    id: str


class Message(MessageIn):
    id: str
    publish_timestamp: datetime
    edit_timestamp: datetime | None = None

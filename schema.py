from pydantic import BaseModel


class MessageIn(BaseModel):
    content: str
    from_user_id: int
    to_user_id: int


class ID(BaseModel):
    id: str


class Message(MessageIn):
    id: str
    publish_timestamp: float
    edit_timestamp: float | None = None

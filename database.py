from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

uri = f"mongodb+srv://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@cluster0.u08cc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = AsyncIOMotorClient(uri)
db = client.Cluster0
messages = db["messages"]

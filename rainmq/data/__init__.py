from motor.motor_asyncio import AsyncIOMotorClient


class MongoClient:
    __client: AsyncIOMotorClient

    @classmethod
    async def initialize(cls, connection_url, database_name):
        cls.__client = AsyncIOMotorClient(connection_url)[database_name]

    @classmethod
    def get_collection(cls, collection_name):
        collection = cls.__client[collection_name]
        return collection

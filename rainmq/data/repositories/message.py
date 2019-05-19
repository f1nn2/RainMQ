from rainmq.data import MongoClient
from rainmq.services.repositories_interface.message import MessageRepository


MESSAGE_COLLECTION = 'message'


class MongoMessageRepository(MessageRepository):
    def __init__(self):
        self.db = MongoClient.get_collection(MESSAGE_COLLECTION)

    async def log(self, message: dict):
        await self.db.insert_one({**message, 'status': 'stored'})

    async def delete(self, message_id: str):
        await self.db.update_one(
            {'id': message_id},
            {'$set': {'status': 'brought'}}
        )

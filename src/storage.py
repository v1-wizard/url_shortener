import time
import uuid

from motor.motor_asyncio import AsyncIOMotorClient

from settings import USH_MONGO_CON_STRING


client = AsyncIOMotorClient(USH_MONGO_CON_STRING)


class Link:
    def __init__(self, link, lid=None, r_count=None, r_at=None):
        """

        :param link: link that should be shorted.
        :param lid: link id  also it is use for create redirect link
        :param r_count: redirect count
        :param r_at: last time when link was used in timestamp format
        """
        self.link = link
        self.lid = lid or uuid.uuid4().hex[:10]
        self.r_count = r_count or 0
        self.r_at = r_at

    def to_dict(self):
        return vars(self)


class NotFoundException(Exception):
    pass


async def insert_link(link):
    await client.db.links.insert_one(link.to_dict())


async def update_link_stats(link):
    link.r_at = time.time()
    link.r_count += 1
    await client.db.links.update_one(
        {'lid': link.lid}, {'$set': link.to_dict()}, upsert=False
    )


async def get_link(link_id):
    document = await client.db.links.find_one({'lid': link_id}, {'_id': False})
    if not document:
        raise NotFoundException()

    return Link(**document)


async def purge_all():
    await client.db.links.delete_many({})


async def get_all_links():
    cursor = client.db.links.find({}, {'_id': False})
    links = [Link(**document) for document in await cursor.to_list(777)]
    return links

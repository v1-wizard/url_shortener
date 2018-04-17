import time
import uuid

from pymongo import MongoClient

from settings import USH_MONGO_CON_STRING


client = MongoClient(USH_MONGO_CON_STRING)
link_collection = client.db.links


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


def insert_link(link):
    link_collection.insert_one(link.to_dict())


def update_link_stats(link):
    link.r_at = time.time()
    link.r_count += 1
    link_collection.update_one(
        {'lid': link.lid}, {'$set': link.to_dict()}, upsert=False
    )


def get_link(link_id):
    result = link_collection.find_one({'lid': link_id}, {'_id': False})
    if not result:
        raise NotFoundException()

    return Link(**result)


def purge_all():
    link_collection.delete_many({})


def get_all_links():
    results = link_collection.find({}, {'_id': False})
    return [Link(**result) for result in results]

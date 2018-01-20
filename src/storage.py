import time
import uuid

from tinydb import TinyDB, where

from settings import USH_DB_PATH


db = TinyDB(USH_DB_PATH)


class Link:
    def __init__(self, link, lid=None, r_count=None, r_at=None):
        """

        :param link: link that should be shorted.
        :param lid: link id  also it is use for create redirect link
        :param r_count: redirect count
        :param r_at: last time when link was used in timestamp format
        """
        self.link = link
        self.lid = lid or str(uuid.uuid4())
        self.r_count = r_count or 0
        self.r_at = r_at

    def to_dict(self):
        return vars(self)


class NotFoundException(Exception):
    pass


def insert_link(link):
    db.insert(link.to_dict())


def update_link_stats(link):
    link.r_at = time.time()
    link.r_count += 1
    db.update(link.to_dict(), where('lid') == link.lid)


def get_link(link_id):
    results = db.search(where('lid') == link_id)
    if len(results) == 0:
        raise NotFoundException()

    return Link(**results[0])


def purge_all():
    db.purge()


def get_all_links():
    results = db.all()
    return [Link(**result) for result in results]

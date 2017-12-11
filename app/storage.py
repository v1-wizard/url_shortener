# -*- coding: utf-8 -*-

import time
import uuid

from tinydb import Query, TinyDB


db = TinyDB('../data/links.json')


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


class NotFoundException(Exception):
    pass


def insert_link(link):
    db.insert(link.__dict__)


async def update_link_stats(link):
    link.r_at = time.time()
    link.r_count += 1
    db.update(link.__dict__, Query().lid == link.lid)


def get_link(link_id):
    results = db.search(Query().lid == link_id)
    if len(results) == 0:
        raise NotFoundException()

    return Link(**results[0])

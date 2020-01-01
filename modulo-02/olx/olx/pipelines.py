# -*- coding: utf-8 -*-
import sqlite3
import pymongo


class OlxSqlitePipeline(object):

    def process_item(self, item, spider):
        self.conn.execute(
            'insert into cars(title, ports, year) values (:title, :ports, :year)',
            item
        )
        self.conn.commit()
        return item

    def create_table(self):
        result = self.conn.execute(
            'select name from sqlite_master where type = "table" and name = "cars"'
        )
        try:
            value = next(result)
        except StopIteration as ex:
            self.conn.execute(
                'create table cars(id integer primary key, title text, ports text, year text)'
            )

    def open_spider(self, spider):
        self.conn = sqlite3.connect('db.sqlite3')
        self.create_table()
    
    def close_spider(self, spider):
        self.conn.close()


class MongoPipeline(object):

    collection_name = 'cars'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from tutorial.items import CartoonItem, SectionItem
from tutorial.settings import sql_host, sql_port, sql_user, sql_passwd, sql_db, collection_manhua, collection_section

class TutorialPipeline:

    def __init__(self):
        try:
            self.client = MongoClient(sql_host, sql_port)
            self.mhpost = self.client[sql_db]
            self.mhpost.authenticate(sql_user, sql_passwd)
            print("MonoDB connection established...")
        except Exception as e:
            print("An exception occurred when try to connect to MongoDB: "+str(e))

    def process_item(self, item, spider):
        if isinstance(item, CartoonItem):
            data = {
                'id': item['id'],
                'name': item['name'],
                'des': item['des'],
                'cover': item['cover'],
                'author': item['author'],
                'status': item['status'],
                'typeTag': item['typeTag'],
                'classTag': item['classTag'],
                'area': item['area'],
                'alias': item['alias'],
                'updateTime': item['updateTime'],
                'chapter': item['chapter']
            }
            self.mhpost[ collection_manhua ].insert_one(data)

        if isinstance(item, SectionItem):
            data = {
                'title': item['title'],
                'name': item['name'],
                'href': item['href'],
                'index': item['index'],
                'picture': item['picture']
            }
            self.mhpost[ collection_section ].insert_one(data)
        return item

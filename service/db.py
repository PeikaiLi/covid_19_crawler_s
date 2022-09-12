"""
@ProjectName: DXY-2019-nCov-Crawler
@FileName: db.py
@Author: Jiabao Lin
@Date: 2020/1/21
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv
# load_dotenv的导入是为了补充一些环境变量 从 .env 文件里面
# Load environment parameters


# uri = '**Confidential**'
# 如果访问本地服务器
# client = MongoClient(host='localhost', port=27017) 
load_dotenv()  # 补充一些环境变量 从 .env 文件里面
client = MongoClient(os.getenv('MONGO_URI'))

db = client['2019-nCoV'] # use 2019-nCoV 有就切换，没有就创建该数据库


class DB:
    def __init__(self):
        self.db = db

    def insert(self, collection, data):
        if type(data) == dict:
            data = [data]
        self.db[collection].insert_many(data)

    def find_one(self, collection, data=None):
        return self.db[collection].find_one(data)

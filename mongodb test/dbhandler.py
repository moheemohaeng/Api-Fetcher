from pymongo import MongoClient
from pymongo.cursor import CursorType



#DB 연결
host = '192.168.1.45'
port = '25017'
mongo = MongoClient(host, int(port))
#print(mongo)


#insert
def insert_item_one(mongo, data, db_name = None, collection_name = None):
    result = mongo[db_name][collection_name].insert_one(data).inserted_id
    return result

def insert_item_many(mongo, datas, db_name = None, collection_name = None):
    result = mongo[db_name][collection_name].insert_many(datas).inserted_ids
    return result

insert_item_one(mongo, {"text":"Hello Python"}, "test","test")




#find
def find_item_one(mongo, condition=None, db_name = None, collection_name = None):
    result =mongo[db_name][collection_name].find_one(condition,{"_id": False})
    return result

def find_item(mongo, condition=None, db_name = None, collection_name = None):
    result = mongo[db_name][collection_name].find(condition, {"_id:": False}, 
    no_cursor_timeout = True, cursor_type = CursorType.EXHAUST)
    return result

cursor = find_item(mongo, None, "test", "test")
for i in cursor:
    print(i["text"])



#delete
def delete_item_one(mongo, condition=None, db_name = None, collection_name = None):
    result = mongo[db_name][collection_name].delete_one(condition)
    return result

def delete_item_many(mongo, condition=None, db_name = None, collection_name = None):
    result = mongo[db_name][collection_name].delete_many(condition)
    return result

# delete_item_one(mongo, {"text":"Hello Python"}, "test", "test")


#text search
def text_search(mongo, text=None, db_name=None, collection_name = None):
    result = mongo[db_name][collection_name].find({"$text": {"Search":text}})
    return result









class DBHandler:
    def __init__(self):
        host = "localhost"
        port = "27017"
        self.client = MongoClient(host, int(port))

    def insert_item_one(self, data, db_name=None, collection_name=None):
        result = self.client[db_name][collection_name].insert_one(data).inserted_id
        return result

    def insert_item_many(self, datas, db_name=None, collection_name=None):
        result = self.client[db_name][collection_name].insert_many(datas).inserted_ids
        return result

    def find_item_one(self, condition=None, db_name=None, collection_name=None):
        result = self.client[db_name][collection_name].find_one(condition, {"_id": False})
        return result

    def find_item(self, condition=None, db_name=None, collection_name=None):
        result = self.client[db_name][collection_name].find(condition, {"_id": False}, no_cursor_timeout=True, cursor_type=CursorType.EXHAUST)
        return result

    def delete_item_one(self, condition=None, db_name=None, collection_name=None):
        result = self.client[db_name][collection_name].delete_one(condition)
        return result

    def delete_item_many(self, condition=None, db_name=None, collection_name=None):
        result = self.client[db_name][collection_name].delete_many(condition)
        return result

    def update_item_one(self, condition=None, update_value=None, db_name=None, collection_name=None):
        result = self.client[db_name][collection_name].update_one(filter=condition, update=update_value)
        return result

    def update_item_many(self, condition=None, update_value=None, db_name=None, collection_name=None):
        result = self.client[db_name][collection_name].update_many(filter=condition, update=update_value)
        return result

    def text_search(self, text=None, db_name=None, collection_name=None):
        result = self.client[db_name][collection_name].find({"$text": {"$search": text}})
        return result



mongo = DBHandler()
#mongo.find_item_one(None, "test", "test")
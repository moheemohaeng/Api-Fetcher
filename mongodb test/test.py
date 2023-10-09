from pymongo import MongoClient
from pymongo.cursor import CursorType



#DB 연결
host = 'localhost'
port = '27017'
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

delete_item_one(mongo, {"text":"Hello Python"}, "test", "test")



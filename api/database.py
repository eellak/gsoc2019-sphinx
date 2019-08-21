from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
dblist = client.list_database_names()
# if "gsoc2019" in dblist:
#    client.drop_database('gsoc2019')
db = client.gsoc2019


def insert_one(collection, data):
    col = db[collection]
    result = col.insert_one(data)
    return result


def insert_many(collection, data):
    col = db[collection]
    result = col.insert_many(data, manipulate=False)
    return result


def update_one(collection, query, data):
    col = db[collection]
    result = col.update_one(query, data)
    return result


def find_one(collection, data):
    col = db[collection]
    result = col.find_one(data)
    return result


def find_many(collection, data):
    col = db[collection]
    result = col.find(data)
    return result


def delete_one(collection, data):
    col = db[collection]
    result = col.delete_one(data)
    return result

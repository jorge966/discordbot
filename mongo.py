from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')

db = client.matchDatabase

collection = db.matches
post = {"account_id": 92576390,
        "match_id": 4758270111
        }

post_id = collection.insert_one(post).inserted_id

remove_id = collection.remove()











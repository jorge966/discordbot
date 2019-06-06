import pymongo
import pprint as pp
from pymongo import MongoClient

# Creates the MongoDB Creation
class mongoConnection:

    # Initalize the Mongo connection
    def __init__(self, ip_address, db_name, coll_name, port='27017'):
        connectionUrl = 'mongodb://{}:{}'.format(ip_address, port)
        client = MongoClient(connectionUrl)
        database = client[db_name]
        self.db = database[coll_name]

    # Insert one object and return ID.
    def insertOne(self, object):
        return self.db.insert_one(object).inserted_id

    # Find first document with specified name
    def findByName(self, object_name):
        return self.db.find_one({ "name": object_name })

    # Get all documents in database
    def getAllDocuments(self):
        return self.db.find()

    # Get all documents matching a filter
    def getAllDocumentsByFilter(self, filter):
        return self.db.find(filter)

    # Get the first document matching filter
    def getOneDocumentByFilter(self, filter):
        return self.db.find_one(filter)
        
    # Updates a specific field in a document that matches the filter
    def updateByField(self, filter, field):
        query = filter
        update = {"$set": field}
        self.db.find_one_and_update(query, update, upsert=True)

    # Insert or Update an entire document by filter
    def upsertOneByField(self, filter, object):
        query = filter
        update = {"$set": object}
        self.db.find_one_and_update(query, update, upsert=True)

    # updates match ID (specific to match only DB's)
    # Jorge refactor this
    def updateOneByMatchid(self, match_id, object):
        query = { "match_id": match_id }
        update = { "$set": { "match_id": object } }
        self.db.update_one(query, update)

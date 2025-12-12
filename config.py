
# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi

# # uri = "mongodb+srv://user:1234@theweddingcompany.lsb4dg9.mongodb.net/?appName=TheWeddingCompany"
# uri = "mongodb+srv://user:1234@theweddingcompany.lsb4dg9.mongodb.net/wedding_master?retryWrites=true&w=majority"

# client = MongoClient(uri, server_api=ServerApi('1'))

# # db = client.organizations
# db = client["wedding_master"]
# org_collection = db['organizations']
# admin_collection = db['admins']


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://user:1234@theweddingcompany.lsb4dg9.mongodb.net/wedding_master?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

master_db = client["wedding_master"]    # REAL DB NAME

org_collection = master_db["organizations"]
admin_collection = master_db["admins"]


import pymongo

class DataEntry:
    def __init__(self, description, submitter, create_date, status, imageResult, prompt, revised_prompt):
        self.description = description
        self.submitter = submitter
        self.create_date = create_date
        self.status = status
        self.imageResult = imageResult
        self.prompt = prompt
        self.revised_prompt = revised_prompt

def get_db(db_name):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client[db_name]
    return db

def get_collection(db, collection_name):
    _collection = db[collection_name]
    return _collection

def insert(collection, data):
    res = collection.insert_one(data)
    print(res)
    _id = res.inserted_id
    print(_id)

def query(collection):
    res = []
    for x in collection.find({}, {"submitter": "xibo"}):
        res.append(x)
    print(res)
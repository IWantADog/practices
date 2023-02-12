from pymongo import MongoClient, database
from pymongo.collation import Collation

client = MongoClient(host='127.0.0.1')
db: database.Database = client['test']

def iter_find():
    c: Collation  = db.get_collection("user")
    items = c.find()
    print(type(items))
    for item in c.find():
        print(item)

def insert():
    users = ["bob", "benji", "tom"]

    c = db.get_collection("record")
    for u in users:
        for i in range(1, 10):
            c.insert_one({"user": u, "count": i})
    

if __name__ == '__main__':
    insert()
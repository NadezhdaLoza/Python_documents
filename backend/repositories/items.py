from utils.database import get_collection

class ItemRepository:
    def __init__(self):
        self.collection = get_collection("items")

    def find_all(self):
        return list(self.collection.find())
    
    def find_one(self, id):
        return self.collection.find_one({"_id": id})

    def insert(self, item):
        return self.collection.insert_one(item)

    def replace(self, id, item):
        return self.collection.replace_one({"_id": id}, item)

    def delete(self, id):
        return self.collection.delete_one({"_id": id})

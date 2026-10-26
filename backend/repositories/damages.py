from utils.database import get_collection

class DamageRepository:
    def __init__(self):
        self.collection = get_collection("damages")

    def find_all(self):
        return list(self.collection.find())
    
    def find_one(self, id):
        return self.collection.find_one({"_id": id})

    def insert(self, damage):
        return self.collection.insert_one(damage)

    def replace(self, id, damage):
        return self.collection.replace_one({"_id": id}, damage)

    def delete(self, id):
        return self.collection.delete_one({"_id": id})
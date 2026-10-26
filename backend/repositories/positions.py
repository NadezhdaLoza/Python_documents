from utils.database import get_collection

class PositionRepository:
    def __init__(self):
        self.collection = get_collection("positions")

    def find_all(self):
        return list(self.collection.find())
    
    def find_one(self, id):
        return self.collection.find_one({"_id": id})

    def insert(self, position):
        return self.collection.insert_one(position)

    def replace(self, id, position):
        return self.collection.replace_one({"_id": id}, position)

    def delete(self, id):
        return self.collection.delete_one({"_id": id})

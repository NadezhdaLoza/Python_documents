from utils.database import get_collection

class IndividualRepository:
    def __init__(self):
        self.collection = get_collection("individuals")

    def find_all(self):
        return list(self.collection.aggregate([
            { "$lookup": {
                "from": "positions",
                "localField": "position",
                "foreignField": "_id",
                "as": "position"
            }},
            { "$unwind": "$position" }
        ]))
    
    def find_one(self, id):
        return list(self.collection.aggregate([
            { "$match": { "_id": id } },
            {
                "$lookup": {
                    "from": "positions",
                    "localField": "position",
                    "foreignField": "_id",
                    "as": "position"
                }
            },
            { "$unwind": "$position" }
        ]))[0]

    def insert(self, individual):
        return self.collection.insert_one(individual)

    def replace(self, id, individual):
        return self.collection.replace_one({"_id": id}, individual)

    def delete(self, id):
        return self.collection.delete_one({"_id": id})

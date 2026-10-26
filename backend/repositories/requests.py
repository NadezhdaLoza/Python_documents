from utils.database import get_collection

class RepairRequestRepository:
    def __init__(self):
        self.collection = get_collection("repair_requests")

    def find_all(self):
        return list(self.collection.aggregate([
            { "$match": { "type": "repair" }},
            { "$lookup": {
                "from": "individuals",
                "localField": "customer",
                "foreignField": "_id",
                "as": "customer"
            }},
            { "$unwind": { "path": "$customer", "preserveNullAndEmptyArrays": True } },
            { "$lookup": {
                "from": "individuals",
                "localField": "contractor",
                "foreignField": "_id",
                "as": "contractor"
            }},
            { "$unwind": { "path": "$contractor", "preserveNullAndEmptyArrays": True } },
            { "$addFields": {
                "date": { "$dateToString": { "format": "%Y-%m-%d", "date": "$date", "timezone": "UTC" } }
            }}
        ]))
    
    def find_one(self, id):
        pipeline = [
            { "$match": { "type": "repair", "_id": id }},
            { "$lookup": {
                "from": "full_repair_requests",
                "localField": "_id",
                "foreignField": "_id",
                "as": "details"
            }},
            { "$unwind": { "path": "$details", "preserveNullAndEmptyArrays": True } },
            { "$unwind": { "path": "$details.items", "preserveNullAndEmptyArrays": True } },
            { "$lookup": {
                "from": "items",
                "localField": "details.items.item",
                "foreignField": "_id",
                "as": "details.items.item"
            }},
            { "$unwind": { "path": "$details.items.item", "preserveNullAndEmptyArrays": True } },
            { "$lookup": {
                "from": "damages",
                "localField": "details.items.damage",
                "foreignField": "_id",
                "as": "details.items.damage"
            }},
            { "$unwind": { "path": "$details.items.damage", "preserveNullAndEmptyArrays": True } },
            { "$group": {
                "_id": "$_id",
                "number": { "$first": "$number" },
                "date": { "$first": "$date" },
                "customer": { "$first": "$customer" },
                "contractor": { "$first": "$contractor" },
                "items": { "$push": "$details.items" }
            }},
            { "$lookup": {
                "from": "individuals",
                "localField": "customer",
                "foreignField": "_id",
                "as": "customer"
            }},
            { "$unwind": { "path": "$customer", "preserveNullAndEmptyArrays": True } },
            { "$lookup": {
                "from": "individuals",
                "localField": "contractor",
                "foreignField": "_id",
                "as": "contractor"
            }},
            { "$unwind": { "path": "$contractor", "preserveNullAndEmptyArrays": True } },
            { "$addFields": {
                "date": { "$dateToString": { "format": "%Y-%m-%d", "date": "$date", "timezone": "UTC" } }
            }}
        ]
        
        result = list(self.collection.aggregate(pipeline))
        return result[0] if result else None

    def insert(self, repair_request):
        return self.collection.insert_one(repair_request)

    def replace(self, id, repair_request):
        return self.collection.replace_one({"_id": id}, repair_request)

    def delete(self, id):
        return self.collection.delete_one({"_id": id})
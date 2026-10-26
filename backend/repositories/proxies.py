from utils.database import get_collection

class ProxyRepository:
    def __init__(self):
        self.collection = get_collection("documents")

    def find_all(self):
        return list(self.collection.aggregate([
            { "$match": { "type": "proxy" }},
            { "$lookup": {
                "from": "organizations",
                "localField": "organization",
                "foreignField": "_id",
                "as": "organization"
            }},
            { "$unwind": "$organization" },
            { "$set": {
                "date": { "$dateToString": {
                    "format": "%Y-%m-%d",
                    "date": "$date"
                }}
            }}
        ]))
    
    def find_one(self, id):
        return list(self.collection.aggregate([
            { "$match": {
                "type": "proxy",
                "_id": id
            }},
            { "$lookup": {
                "from": "full_documents",
                "localField": "_id",
                "foreignField": "_id",
                "as": "details"
            }},
            { "$unwind": "$details" },
            { "$unwind": "$details.items" },
            { "$lookup": {
                "from": "items",
                "localField": "details.items.item",
                "foreignField": "_id",
                "as": "details.items.item"
            }},
            { "$unwind": {
                "path": "$details.items.item"
            }},
            { "$group": {
                "_id": "$_id",
                "number": { "$first": "$number" },
                "date": { "$first": "$date" },
                "organization": { "$first": "$organization" },
                "supplier_organization": { "$first": "$details.supplier_organization" },
                "individual": { "$first": "$details.individual" },
                "period": { "$first": "$details.period" },
                "items": { "$push": "$details.items" }
            }},
            { "$lookup": {
                "from": "individuals",
                "localField": "individual",
                "foreignField": "_id",
                "as": "individual"
            }},
            { "$unwind": "$individual" },
            { "$lookup": {
                "from": "organizations",
                "localField": "organization",
                "foreignField": "_id",
                "as": "organization"
            }},
            { "$unwind": "$organization" },
            { "$lookup": {
                "from": "organizations",
                "localField": "supplier_organization",
                "foreignField": "_id",
                "as": "supplier_organization"
            }},
            { "$unwind": "$supplier_organization" },
            { "$set": {
                "date": { "$dateToString": {
                    "format": "%Y-%m-%d",
                    "date": "$date"
                }},
                "period.from": { "$dateToString": {
                    "format": "%Y-%m-%d",
                    "date": "$period.from"
                }},
                "period.until": { "$dateToString": {
                    "format": "%Y-%m-%d",
                    "date": "$period.until"
                }}
            }}
        ]))[0]

    def insert(self, proxy):
        return self.collection.insert_one(proxy)

    def replace(self, id, proxy):
        return self.collection.replace_one({"_id": id}, proxy)

    def delete(self, id):
        return self.collection.delete_one({"_id": id})


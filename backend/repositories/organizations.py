from utils.database import get_collection

class OrganizationRepository:
    def __init__(self):
        self.collection = get_collection("organizations")

    def find_all(self):
        return list(self.collection.find())
    
    def find_one(self, id):
        return self.collection.find_one({"_id": id})

    def insert(self, organization):
        return self.collection.insert_one(organization)

    def replace(self, id, organization):
        return self.collection.replace_one({"_id": id}, organization)

    def delete(self, id):
        return self.collection.delete_one({"_id": id})

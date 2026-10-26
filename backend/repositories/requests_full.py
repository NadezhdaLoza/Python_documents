from utils.database import get_collection

class FullRepairRequestRepository:
    def __init__(self):
        self.collection = get_collection("full_repair_requests")

    def insert(self, repair_request_full):
        return self.collection.insert_one(repair_request_full)

    def update(self, id, repair_request_full):
        return self.collection.replace_one({"_id": id}, repair_request_full)

    def replace(self, id, repair_request_full):
        return self.collection.replace_one({"_id": id}, repair_request_full)

    def delete(self, id):
        return self.collection.delete_one({"_id": id})
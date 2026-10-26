from utils.database import get_collection

class ProxyFullRepository:
    def __init__(self):
        self.collection = get_collection("full_documents")

    def insert(self, proxy_full):
        return self.collection.insert_one(proxy_full)

    def update(self, id, proxy_full):
        return self.collection.replace_one({"_id": id}, proxy_full)

    def replace(self, id, proxy_full):
        return self.collection.replace_one({"_id": id}, proxy_full)

    def delete(self, id):
        return self.collection.delete_one({"_id": id})

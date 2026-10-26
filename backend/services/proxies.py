from bson import ObjectId
from datetime import datetime

from repositories.proxies import ProxyRepository
from repositories.proxies_full import ProxyFullRepository
from utils.error_handler import ErrorHandler

class ProxyService:
    def __init__(self):
        self.documents_repository = ProxyRepository()
        self.documents_full_repository = ProxyFullRepository()
        self.error_handler = ErrorHandler()

    def get_all(self):
        proxies = self.documents_repository.find_all()
        return proxies
    
    def get_one(self, id):
        self.error_handler.validate_object_id(id)
        proxy = self.documents_repository.find_one(ObjectId(id))
        return proxy
    
    def create(self, data):
        self.error_handler.validate_required_fields(data, [
            "number",
            "date",
            "organization",
            "supplier_organization",
            "individual",
            "period",
            "items"
        ])
        self.error_handler.validate_required_fields(data["period"], ["from", "until"])
        for item in data["items"]:
            self.error_handler.validate_required_fields(item, ["count", "item"])
            self.error_handler.validate_int_field(item["count"], "items.count")
            self.error_handler.validate_object_id(item["item"])
        self.error_handler.validate_date_field(data["date"], "date")
        self.error_handler.validate_date_field(data["period"]["from"], "period.from")
        self.error_handler.validate_date_field(data["period"]["until"], "period.until")
        self.error_handler.validate_object_id(data["organization"])
        self.error_handler.validate_object_id(data["supplier_organization"])
        self.error_handler.validate_object_id(data["individual"]),
        self.error_handler.validate_string_field(data["number"], "number")

        proxy = {
            "number": data["number"].strip(),
            "date": datetime.strptime(data["date"], "%Y-%m-%d"),
            "organization": ObjectId(data["organization"]),
            "type": "proxy"
        }

        result = self.documents_repository.insert(proxy)

        proxy_full = {
            "_id": result.inserted_id,
            "supplier_organization": ObjectId(data["supplier_organization"]),
            "individual": ObjectId(data["individual"]),
            "period": {
                "from": datetime.strptime(data["period"]["from"], "%Y-%m-%d"),
                "until": datetime.strptime(data["period"]["until"], "%Y-%m-%d")
            },
            "items": list({ "count": int(item["count"]), "item": ObjectId(item["item"])} for item in data["items"])
        }

        result = self.documents_full_repository.insert(proxy_full)

        return { "_id": result.inserted_id }

    def update(self, data):
        self.error_handler.validate_required_fields(data, [
            "_id",
            "number",
            "date",
            "organization",
            "supplier_organization",
            "individual",
            "period",
            "items"
        ])
        self.error_handler.validate_required_fields(data["period"], ["from", "until"])
        for item in data["items"]:
            self.error_handler.validate_required_fields(item, ["count", "item"])
            self.error_handler.validate_int_field(item["count"], "items.count")
            self.error_handler.validate_object_id(item["item"])
        self.error_handler.validate_object_id(data["_id"]),
        self.error_handler.validate_date_field(data["date"], "date")
        self.error_handler.validate_date_field(data["period"]["from"], "period.from")
        self.error_handler.validate_date_field(data["period"]["until"], "period.until")
        self.error_handler.validate_object_id(data["organization"])
        self.error_handler.validate_object_id(data["supplier_organization"])
        self.error_handler.validate_object_id(data["individual"]),
        self.error_handler.validate_string_field(data["number"], "number")
        
        id = ObjectId(data["_id"])
        proxy = {
            "number": data["number"].strip(),
            "date": datetime.strptime(data["date"], "%Y-%m-%d"),
            "organization": ObjectId(data["organization"]),
            "type": "proxy"
        }

        result = self.documents_repository.replace(id, proxy)

        proxy_full = {
            "supplier_organization": ObjectId(data["supplier_organization"]),
            "individual": ObjectId(data["individual"]),
            "period": {
                "from": datetime.strptime(data["period"]["from"], "%Y-%m-%d"),
                "until": datetime.strptime(data["period"]["until"], "%Y-%m-%d")
            },
            "items": list({ "count": int(item["count"]), "item": ObjectId(item["item"])} for item in data["items"])
        }

        result = self.documents_full_repository.replace(id, proxy_full)
        self.error_handler.validate_document(result.matched_count)
        return { "success": True }

    def delete(self, id):
        self.error_handler.validate_object_id(id)
        result = self.documents_repository.delete(ObjectId(id))
        result = self.documents_full_repository.delete(ObjectId(id))
        return { "success": True }

from bson import ObjectId
from datetime import datetime

from repositories.requests import RepairRequestRepository
from repositories.requests_full import FullRepairRequestRepository
from utils.error_handler import ErrorHandler

class RepairRequestService:
    def __init__(self):
        self.repository = RepairRequestRepository()
        self.full_repository = FullRepairRequestRepository()
        self.error_handler = ErrorHandler()

    def get_all(self):
        requests = self.repository.find_all()
        return requests
    
    def get_one(self, id):
        self.error_handler.validate_object_id(id)
        request = self.repository.find_one(ObjectId(id))
        return request
    
    def create(self, data):
        self.error_handler.validate_required_fields(data, [
            "number",
            "date",
            "customer",
            "contractor",
            "items"
        ])
        for item in data["items"]:
            self.error_handler.validate_required_fields(item, [
                "number",
                "item",
                "purchase_date",
                "commissioning_date",
                "actual_service_life",
                "damage",
                "damage_circumstances"
            ])
            self.error_handler.validate_int_field(item["number"], "items.number")
            self.error_handler.validate_object_id(item["item"])
            self.error_handler.validate_date_field(item["purchase_date"], "items.purchase_date")
            self.error_handler.validate_date_field(item["commissioning_date"], "items.commissioning_date")
            self.error_handler.validate_float_field(item["actual_service_life"], "items.actual_service_life")
            self.error_handler.validate_object_id(item["damage"])
            self.error_handler.validate_string_field(item["damage_circumstances"], "items.damage_circumstances")
        self.error_handler.validate_date_field(data["date"], "date")
        self.error_handler.validate_object_id(data["customer"])
        self.error_handler.validate_object_id(data["contractor"])
        self.error_handler.validate_string_field(data["number"], "number")

        request = {
            "number": data["number"].strip(),
            "date": datetime.strptime(data["date"], "%Y-%m-%d"),
            "customer": ObjectId(data["customer"]),
            "contractor": ObjectId(data["contractor"]),
            "type": "repair"
        }

        result = self.repository.insert(request)

        full_request = {
            "_id": result.inserted_id,
            "items": list({
                "number": int(item["number"]),
                "item": ObjectId(item["item"]),
                "purchase_date": datetime.strptime(item["purchase_date"], "%Y-%m-%d"),
                "commissioning_date": datetime.strptime(item["commissioning_date"], "%Y-%m-%d"),
                "actual_service_life": float(item["actual_service_life"]),
                "damage": ObjectId(item["damage"]),
                "damage_circumstances": item["damage_circumstances"].strip()
            } for item in data["items"]),
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        result = self.full_repository.insert(full_request)

        return { "_id": result.inserted_id }

    def update(self, data):
        self.error_handler.validate_required_fields(data, [
            "_id",
            "number",
            "date",
            "customer",
            "contractor",
            "items"
        ])
        for item in data["items"]:
            self.error_handler.validate_required_fields(item, [
                "number",
                "item",
                "purchase_date",
                "commissioning_date",
                "actual_service_life",
                "damage",
                "damage_circumstances"
            ])
            self.error_handler.validate_int_field(item["number"], "items.number")
            self.error_handler.validate_object_id(item["item"])
            self.error_handler.validate_date_field(item["purchase_date"], "items.purchase_date")
            self.error_handler.validate_date_field(item["commissioning_date"], "items.commissioning_date")
            self.error_handler.validate_float_field(item["actual_service_life"], "items.actual_service_life")
            self.error_handler.validate_object_id(item["damage"])
            self.error_handler.validate_string_field(item["damage_circumstances"], "items.damage_circumstances")
        self.error_handler.validate_object_id(data["_id"])
        self.error_handler.validate_date_field(data["date"], "date")
        self.error_handler.validate_object_id(data["customer"])
        self.error_handler.validate_object_id(data["contractor"])
        self.error_handler.validate_string_field(data["number"], "number")
        
        id = ObjectId(data["_id"])
        request = {
            "number": data["number"].strip(),
            "date": datetime.strptime(data["date"], "%Y-%m-%d"),
            "customer": ObjectId(data["customer"]),
            "contractor": ObjectId(data["contractor"]),
            "type": "repair"
        }

        result = self.repository.replace(id, request)

        full_request = {
            "_id": id,
            "items": list({
                "number": int(item["number"]),
                "item": ObjectId(item["item"]),
                "purchase_date": datetime.strptime(item["purchase_date"], "%Y-%m-%d"),
                "commissioning_date": datetime.strptime(item["commissioning_date"], "%Y-%m-%d"),
                "actual_service_life": float(item["actual_service_life"]),
                "damage": ObjectId(item["damage"]),
                "damage_circumstances": item["damage_circumstances"].strip()
            } for item in data["items"]),
            "updated_at": datetime.now()
        }

        result = self.full_repository.replace(id, full_request)
        self.error_handler.validate_document(result.matched_count)
        return { "success": True }

    def delete(self, id):
        self.error_handler.validate_object_id(id)
        result = self.repository.delete(ObjectId(id))
        result = self.full_repository.delete(ObjectId(id))
        return { "success": True }
from bson import ObjectId
from repositories.organizations import OrganizationRepository
from utils.error_handler import ErrorHandler


class OrganizationService:
    def __init__(self):
        self.repository = OrganizationRepository()
        self.error_handler = ErrorHandler()

    def get_all(self):
        organizations = self.repository.find_all()
        return organizations
    
    def get_one(self, id):
        self.error_handler.validate_object_id(id)
        organization = self.repository.find_one(ObjectId(id))
        return organization
    
    def create(self, data):
        self.error_handler.validate_required_fields(data, ["title", "address"])
        self.error_handler.validate_string_field(data["title"], "title")
        self.error_handler.validate_string_field(data["address"], "address")

        organization = {
            "title": data["title"].strip(),
            "address": data["address"].strip()
        }
        
        result = self.repository.insert(organization)
        return { "_id": result.inserted_id }

    def update(self, data):
        self.error_handler.validate_required_fields(data, ["_id", "title", "address"])
        self.error_handler.validate_object_id(data["_id"])
        self.error_handler.validate_string_field(data["title"], "title")
        self.error_handler.validate_string_field(data["address"], "address")
        
        id = ObjectId(data["_id"])
        organization = {
            "title": data["title"].strip(),
            "address": data["address"].strip()
        }

        result = self.repository.replace(id, organization)
        self.error_handler.validate_document(result.matched_count)
        return { "success": True }

    def delete(self, id):
        self.error_handler.validate_object_id(id)
        result = self.repository.delete(ObjectId(id))
        self.error_handler.validate_document(result.deleted_count)
        return { "success": True }
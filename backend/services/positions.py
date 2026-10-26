from bson import ObjectId
from repositories.positions import PositionRepository
from utils.error_handler import ErrorHandler

class PositionService:
    def __init__(self):
        self.repository = PositionRepository()
        self.error_handler = ErrorHandler()

    def get_all(self):
        positions = self.repository.find_all()
        return positions
    
    def get_one(self, id):
        self.error_handler.validate_object_id(id)
        position = self.repository.find_one(ObjectId(id))
        return position
    
    def create(self, data):
        self.error_handler.validate_required_fields(data, ["title"])
        self.error_handler.validate_string_field(data["title"], "title")

        position = { "title": data["title"].strip() }
        result = self.repository.insert(position)
        return { "_id": result.inserted_id }

    def update(self, data):
        self.error_handler.validate_required_fields(data, ["_id", "title"])
        self.error_handler.validate_object_id(data["_id"])
        self.error_handler.validate_string_field(data["title"], "title")
        
        id = ObjectId(data["_id"])
        position = { "title": data["title"].strip() }

        result = self.repository.replace(id, position)
        self.error_handler.validate_document(result.matched_count)
        return { "success": True }

    def delete(self, id):
        self.error_handler.validate_object_id(id)
        result = self.repository.delete(ObjectId(id))
        self.error_handler.validate_document(result.deleted_count)
        return { "success": True }

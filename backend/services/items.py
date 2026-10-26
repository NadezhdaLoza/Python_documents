from bson import ObjectId
from repositories.items import ItemRepository
from utils.error_handler import ErrorHandler


class ItemService:
    def __init__(self):
        self.repository = ItemRepository()
        self.error_handler = ErrorHandler()

    def get_all(self):
        items = self.repository.find_all()
        return items
    
    def get_one(self, id):
        self.error_handler.validate_object_id(id)
        item = self.repository.find_one(ObjectId(id))
        return item
    
    def create(self, data):
        self.error_handler.validate_required_fields(data, ["title"])
        self.error_handler.validate_string_field(data["title"], "title")

        item = { "title": data["title"].strip() }
        result = self.repository.insert(item)
        return { "_id": result.inserted_id }

    def update(self, data):
        self.error_handler.validate_required_fields(data, ["_id", "title"])
        self.error_handler.validate_object_id(data["_id"])
        self.error_handler.validate_string_field(data["title"], "title")
        
        id = ObjectId(data["_id"])
        item = { "title": data["title"].strip() }

        result = self.repository.replace(id, item)
        self.error_handler.validate_document(result.matched_count)
        return { "success": True }

    def delete(self, id):
        self.error_handler.validate_object_id(id)
        result = self.repository.delete(ObjectId(id))
        self.error_handler.validate_document(result.deleted_count)
        return { "success": True }

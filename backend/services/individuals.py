from bson import ObjectId
from repositories.individuals import IndividualRepository
from utils.error_handler import ErrorHandler


class IndividualService:
    def __init__(self):
        self.repository = IndividualRepository()
        self.error_handler = ErrorHandler()

    def get_all(self):
        individuals = self.repository.find_all()
        return individuals
    
    def get_one(self, id):
        self.error_handler.validate_object_id(id)
        individual = self.repository.find_one(ObjectId(id))
        return individual
    
    def create(self, data):
        self.error_handler.validate_required_fields(data, ["lastname", "firstname", "patronymic", "position"])
        self.error_handler.validate_string_field(data["lastname"], "lastname")
        self.error_handler.validate_string_field(data["firstname"], "firstname")
        self.error_handler.validate_string_field(data["patronymic"], "patronymic")
        self.error_handler.validate_object_id(data["position"])

        individual = {
            "lastname": data["lastname"].strip(),
            "firstname": data["firstname"].strip(),
            "patronymic": data["patronymic"].strip(),
            "position": ObjectId(data["position"])
        }

        result = self.repository.insert(individual)
        return { "_id": result.inserted_id }

    def update(self, data):
        self.error_handler.validate_required_fields(data, ["_id", "lastname", "firstname", "patronymic", "position"])
        self.error_handler.validate_object_id(data["_id"])
        self.error_handler.validate_string_field(data["lastname"], "lastname")
        self.error_handler.validate_string_field(data["firstname"], "firstname")
        self.error_handler.validate_string_field(data["patronymic"], "patronymic")
        self.error_handler.validate_object_id(data["position"])
        
        id = ObjectId(data["_id"])
        individual = {
            "lastname": data["lastname"].strip(),
            "firstname": data["firstname"].strip(),
            "patronymic": data["patronymic"].strip(),
            "position": ObjectId(data["position"])
        }

        result = self.repository.replace(id, individual)
        self.error_handler.validate_document(result.matched_count)
        return { "success": True }

    def delete(self, id):
        self.error_handler.validate_object_id(id)
        result = self.repository.delete(ObjectId(id))
        self.error_handler.validate_document(result.deleted_count)
        return { "success": True }
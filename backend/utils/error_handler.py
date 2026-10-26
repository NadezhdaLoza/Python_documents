from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime

class ErrorHandler:
    @staticmethod
    def validate_float_field(value: any, field_name: str):
        if not isinstance(value, (int, float)):
            raise ValueError(f"{field_name} must be a number")
        if float(value) < 0:
            raise ValueError(f"{field_name} cannot be less than zero")
            
    @staticmethod
    def validate_object_id(id: str):
        if not isinstance(id, str):
            raise ValueError("_id must be a string")
        try:
            ObjectId(id)
        except InvalidId:
            raise ValueError("Invalid _id format")

    @staticmethod
    def validate_string_field(value: any, field_name: str):
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")
        stripped = value.strip()
        if len(stripped) == 0:
            raise ValueError(f"{field_name} cannot be empty")
        
    @staticmethod
    def validate_int_field(value: any, field_name: str):
        if not isinstance(value, int):
            raise ValueError(f"{field_name} must be a integer")
        if int(value) < 1:
            raise ValueError(f"{field_name} cannot be less than one")
    
    @staticmethod
    def validate_date_field(value: any, field_name: str):
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")
        stripped = value.strip()
        if len(stripped) == 0:
            raise ValueError(f"{field_name} cannot be empty")
        date = datetime.strptime(stripped, "%Y-%m-%d")

    @staticmethod
    def validate_required_fields(data: dict, fields: list):
        for field in fields:
            if field not in data:
                raise ValueError(f"Required field missing: {field}")
    
    @staticmethod
    def validate_document(count: dict):
        if count == 0:
            raise ValueError("Document with same _id not found")
    

from flask.json.provider import DefaultJSONProvider
from bson import ObjectId
from datetime import datetime

class MongoJSONEncoder(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

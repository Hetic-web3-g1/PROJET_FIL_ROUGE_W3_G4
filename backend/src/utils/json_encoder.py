import json
import uuid
from datetime import datetime

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, uuid.UUID)):
            return str(obj)
        return super().default(obj)

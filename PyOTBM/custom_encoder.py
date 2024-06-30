import json
from lib.otbm_node import OTBMNodeType

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, OTBMNodeType):
            return obj.name
        return super().default(obj)

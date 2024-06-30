from lib.otbm_node import OTBMNode
from const import OTBMNodeType

class OTBMMapData(OTBMNode):
    def __init__(self):
        super().__init__()
        self._type = OTBMNodeType.OTBM_MAP_DATA

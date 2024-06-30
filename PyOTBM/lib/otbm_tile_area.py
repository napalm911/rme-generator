from lib.otbm_node_with_position import OTBMNodeWithPosition
from const import OTBMNodeType

class OTBMTileArea(OTBMNodeWithPosition):
    def __init__(self):
        super().__init__()
        self._type = OTBMNodeType.OTBM_TILE_AREA

    def as_raw_object(self, get_full_branch=True):
        sup_values = super().as_raw_object(get_full_branch)
        return {
            'z': self._z,
            **sup_values
        }

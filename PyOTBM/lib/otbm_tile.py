from lib.bytes import Byt3s
from lib.otbm_node_with_position import OTBMNodeWithPosition
from const import OTBMNodeType

class OTBMTile(OTBMNodeWithPosition):
    def __init__(self):
        super().__init__()
        self._type = OTBMNodeType.OTBM_TILE

    @property
    def real_x(self):
        return self._parent.x + self._x if self._parent else -1

    @property
    def real_y(self):
        return self._parent.y + self._y if self._parent else -1

    @property
    def z(self):
        return self._parent.z if self._parent else -1

    def set(self, otbm_buffer: Byt3s):
        self._x = otbm_buffer.escape_read_byte()
        self._y = otbm_buffer.escape_read_byte()

    def as_raw_object(self, get_full_branch=True):
        sup_values = super().as_raw_object(get_full_branch)
        return {
            'real_x': self.real_x,
            'real_y': self.real_y,
            'z': self.z,
            **sup_values,
        }

from lib.bytes import Byt3s
from lib.otbm_node_with_position import OTBMNodeWithPosition
from const import OTBMNodeType

class OTBMWaypoint(OTBMNodeWithPosition):
    def __init__(self):
        super().__init__()
        self._type = OTBMNodeType.OTBM_WAYPOINT
        self._name = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def set(self, otbm_buffer: Byt3s):
        self._name = otbm_buffer.escape_read_string()
        self._x = otbm_buffer.escape_read_uint16_le()
        self._y = otbm_buffer.escape_read_uint16_le()
        self._z = otbm_buffer.escape_read_byte()

    def as_raw_object(self, get_full_branch=True):
        sup_values = super().as_raw_object(get_full_branch)
        return {
            'name': self._name,
            **sup_values
        }

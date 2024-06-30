from lib.bytes import Byt3s
from lib.otbm_tile import OTBMTile
from const import OTBMNodeType

class OTBMHouseTile(OTBMTile):
    def __init__(self):
        super().__init__()
        self._type = OTBMNodeType.OTBM_HOUSETILE
        self._house_id = None

    @property
    def house_id(self):
        return self._house_id

    @house_id.setter
    def house_id(self, value):
        self._house_id = value

    def set(self, otbm_buffer: Byt3s):
        self._x = otbm_buffer.escape_read_byte()
        self._y = otbm_buffer.escape_read_byte()
        self._house_id = otbm_buffer.escape_read_uint32_le()

    def as_raw_object(self, get_full_branch=True):
        sup_values = super().as_raw_object(get_full_branch)
        return {
            'house_id': self._house_id,
            **sup_values,
        }

from lib.bytes import Byt3s
from lib.otbm_node import OTBMNode
from const import OTBMNodeType

class OTBMItem(OTBMNode):
    def __init__(self):
        super().__init__()
        self._type = OTBMNodeType.OTBM_ITEM
        self._id = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def set(self, otbm_buffer: Byt3s):
        self.id = otbm_buffer.escape_read_uint16_le()

    def as_raw_object(self, get_full_branch=True):
        sup_values = super().as_raw_object(get_full_branch)
        return {
            'id': self._id,
            **sup_values,
        }

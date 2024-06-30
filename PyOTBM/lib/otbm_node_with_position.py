from lib.bytes import Byt3s
from lib.otbm_node import OTBMNode

class OTBMNodeWithPosition(OTBMNode):
    def __init__(self):
        super().__init__()
        self._x = None
        self._y = None
        self._z = None

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value

    def set(self, otbm_buffer: Byt3s):
        self._x = otbm_buffer.escape_read_uint16_le()
        self._y = otbm_buffer.escape_read_uint16_le()
        self._z = otbm_buffer.escape_read_byte()

    def as_raw_object(self, get_full_branch=True):
        sup_values = super().as_raw_object(get_full_branch)
        return {
            'x': self._x,
            'y': self._y,
            **sup_values
        }

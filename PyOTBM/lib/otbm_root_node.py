from lib.bytes import Byt3s
from lib.otbm_node import OTBMNode
from const import OTBMMapVersion, OTBMNodeType

class OTBMRootNode(OTBMNode):
    def __init__(self):
        super().__init__()
        self._type = OTBMNodeType.OTBM_MAP_HEADER
        self._version = None
        self._width = None
        self._height = None
        self._item_major_version = None
        self._item_minor_version = None

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        if value > OTBMMapVersion.MAP_OTBM_3.value:
            raise ValueError(f"Map version cannot be greater than {OTBMMapVersion.MAP_OTBM_3.value}")
        self._version = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def item_major_version(self):
        return self._item_major_version

    @item_major_version.setter
    def item_major_version(self, value):
        self._item_major_version = value

    @property
    def item_minor_version(self):
        return self._item_minor_version

    @item_minor_version.setter
    def item_minor_version(self, value):
        self._item_minor_version = value

    def set(self, node_buffer: Byt3s):
        self.version = node_buffer.escape_read_uint32_le()
        self._width = node_buffer.escape_read_uint16_le()
        self._height = node_buffer.escape_read_uint16_le()
        self._item_major_version = node_buffer.escape_read_uint32_le()
        self._item_minor_version = node_buffer.escape_read_uint32_le()

    def as_raw_object(self, get_full_branch=True):
        sup_values = super().as_raw_object(get_full_branch)
        return {
            **sup_values,
            'version': self.version,
            'width': self._width,
            'height': self._height,
            'item_major_version': self._item_major_version,
            'item_minor_version': self._item_minor_version,
        }

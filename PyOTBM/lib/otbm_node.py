from lib.bytes import Byt3s
from const import OTBMAttribute, OTBMNodeType, OTBMTileState, OTBMNodeSpecialByte

class OTBMNode:
    def __init__(self):
        self._type = None
        self._attributes = {}
        self._parent = None
        self._children = []
        self._prev_sibling = None
        self._next_sibling = None

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, value):
        self._attributes = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def children(self):
        return self._children

    @property
    def prev_sibling(self):
        return self._prev_sibling

    @prev_sibling.setter
    def prev_sibling(self, value):
        self._prev_sibling = value

    @property
    def next_sibling(self):
        return self._next_sibling

    @next_sibling.setter
    def next_sibling(self, value):
        self._next_sibling = value

    @property
    def first_child(self):
        return self._children[0] if self._children else None

    @property
    def last_child(self):
        return self._children[-1] if self._children else None

    def add_child(self, node):
        self._children.append(node)

    def remove_child(self, node):
        if node in self._children:
            self._children.remove(node)
            return True
        return False

    def set_attributes(self, otbm_buffer: Byt3s, otbm_node_end_pos):
        while otbm_buffer.position < otbm_node_end_pos:
            byte = otbm_buffer.read_byte()

            if byte == OTBMAttribute.TEXT.value:
                if otbm_buffer.peek_byte() not in [OTBMNodeSpecialByte.START.value, OTBMNodeSpecialByte.END.value]:
                    self._attributes['text'] = otbm_buffer.escape_read_string()
                else:
                    self._attributes['subType'] = byte

            elif byte == OTBMAttribute.EXT_SPAWN_FILE.value:
                if (otbm_buffer.position + otbm_buffer.escape_peek_uint16_le()) <= otbm_node_end_pos:
                    self._attributes['spawnFile'] = otbm_buffer.escape_read_string()
                else:
                    self._attributes['subType'] = byte

            elif byte == OTBMAttribute.EXT_HOUSE_FILE.value:
                if (otbm_buffer.position + otbm_buffer.escape_peek_uint16_le()) <= otbm_node_end_pos:
                    self._attributes['houseFile'] = otbm_buffer.escape_read_string()
                else:
                    self._attributes['subType'] = byte

            elif byte == OTBMAttribute.HOUSEDOORID.value:
                if (otbm_buffer.position + 1) <= otbm_node_end_pos:
                    self._attributes['houseDoorId'] = otbm_buffer.escape_read_byte()
                else:
                    self._attributes['subType'] = byte

            elif byte == OTBMAttribute.DESCRIPTION.value:
                if otbm_buffer.peek_byte() not in [OTBMNodeSpecialByte.START.value, OTBMNodeSpecialByte.END.value]:
                    if 'description' not in self._attributes:
                        self._attributes['description'] = []
                    self._attributes['description'].append(otbm_buffer.escape_read_string())
                else:
                    self._attributes['subType'] = byte

            elif byte == OTBMAttribute.DESC.value:
                if (otbm_buffer.position + otbm_buffer.escape_peek_uint16_le()) <= otbm_node_end_pos:
                    self._attributes['desc'] = otbm_buffer.escape_read_string()
                else:
                    self._attributes['subType'] = byte

            elif byte == OTBMAttribute.DEPOT_ID.value:
                if (otbm_buffer.position + 2) <= otbm_node_end_pos:
                    self._attributes['depotId'] = otbm_buffer.escape_read_uint16_le()
                else:
                    self._attributes['subType'] = byte

            elif byte == OTBMAttribute.TILE_FLAGS.value:
                if (otbm_buffer.position + 4) <= otbm_node_end_pos:
                    flag_int = otbm_buffer.escape_read_uint32_le()
                    self._attributes['tileFlags'] = {
                        'protection': (flag_int & OTBMTileState.TILESTATE_PROTECTIONZONE.value) == OTBMTileState.TILESTATE_PROTECTIONZONE.value,
                        'noPVP': (flag_int & OTBMTileState.TILESTATE_NOPVP.value) == OTBMTileState.TILESTATE_NOPVP.value,
                        'noLogout': (flag_int & OTBMTileState.TILESTATE_NOLOGOUT.value) == OTBMTileState.TILESTATE_NOLOGOUT.value,
                        'PVPZone': (flag_int & OTBMTileState.TILESTATE_PVPZONE.value) == OTBMTileState.TILESTATE_PVPZONE.value,
                        'refresh': (flag_int & OTBMTileState.TILESTATE_REFRESH.value) == OTBMTileState.TILESTATE_REFRESH.value
                    }
                else:
                    self._attributes['subType'] = byte

            elif byte == OTBMAttribute.RUNE_CHARGES.value:
                if (otbm_buffer.position + 1) <= otbm_node_end_pos:
                    self._attributes['runeCharges'] = otbm_buffer.escape_read_byte()
                else:
                    self._attributes['subType'] = byte

            elif byte == OTBMAttribute.COUNT.value:
                if (otbm_buffer.position + 1) <= otbm_node_end_pos:
                    self._attributes['count'] = otbm_buffer.escape_read_byte()
                else:
                    self._attributes['subType'] = byte

            elif byte == OTBMAttribute.ITEM.value:
                if (otbm_buffer.position + 2) <= otbm_node_end_pos:
                    self._attributes['tileId'] = otbm_buffer.escape_read_uint16_le()
                else:
                    self._attributes['subType'] = byte

            elif byte == OTBMAttribute.ACTION_ID.value:
                if (otbm_buffer.position + 2) <= otbm_node_end_pos:
                    self._attributes['actionId'] = otbm_buffer.escape_read_uint16_le()
                else:
                    self._attributes['subType'] = byte

            elif byte == OTBMAttribute.UNIQUE_ID.value:
                if (otbm_buffer.position + 2) <= otbm_node_end_pos:
                    self._attributes['uniqueId'] = otbm_buffer.escape_read_uint16_le()
                else:
                    self._attributes['subType'] = byte

            elif byte == OTBMAttribute.TELE_DEST.value:
                if (otbm_buffer.position + 5) <= otbm_node_end_pos:
                    self._attributes['destination'] = {
                        "x": otbm_buffer.escape_read_uint16_le(),
                        "y": otbm_buffer.escape_read_uint16_le(),
                        "z": otbm_buffer.escape_read_byte()
                    }
                else:
                    self._attributes['subType'] = byte

            elif byte == OTBMAttribute.CHARGES.value:
                if (otbm_buffer.position + 2) <= otbm_node_end_pos:
                    self._attributes['charges'] = otbm_buffer.escape_read_uint16_le()
                else:
                    self._attributes['subType'] = byte

            elif byte == OTBMAttribute.ATTRIBUTE_MAP.value:
                print('Attribute map, not yet implemented.')
                otbm_buffer.position = otbm_node_end_pos

            else:
                self._attributes['subType'] = byte

    def is_item(self):
        return self._type == OTBMNodeType.OTBM_ITEM

    def get_full_branch(self, as_raw_object=False):
        children = []
        for child in self._children:
            if as_raw_object:
                children.append(child.as_raw_object())
            else:
                children.append(child)
        return children

    def as_raw_object(self, get_full_branch=True):
        return {
            'type': self._type,
            'attributes': self._attributes,
            **({'children': self.get_full_branch(get_full_branch)} if get_full_branch else {})
        }

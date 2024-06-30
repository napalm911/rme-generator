from lib.bytes import Byt3s
from lib.otbm_node import OTBMNode
from lib.otbm_house_tile import OTBMHouseTile
from lib.otbm_item import OTBMItem
from lib.otbm_map_data import OTBMMapData
from lib.otbm_root_node import OTBMRootNode
from lib.otbm_tile import OTBMTile
from lib.otbm_tile_area import OTBMTileArea
from lib.otbm_town import OTBMTown
from lib.otbm_waypoint import OTBMWaypoint
from const import OTBMNodeType, OTBMAttribute, OTBMTileState

class OTBMWriter:
    def __init__(self, root: OTBMRootNode):
        self.tree = root
        self.buffer = Byt3s(100000000)

    def write_buffer(self):
        self.buffer = Byt3s(100000000)
        self.buffer.escape_write_uint32_le(0)  # Write magic bytes
        self._write_node(self.tree)
        return self.buffer.data[:self.buffer.position]

    def _write_node(self, node: OTBMNode):
        if node is None:
            raise ValueError('Node is undefined')

        self.buffer.write_byte(0xFE)
        self.buffer.escape_write_byte(node.type.value)

        if node.type == OTBMNodeType.OTBM_MAP_HEADER:
            self._write_root_node(node)
        elif node.type == OTBMNodeType.OTBM_MAP_DATA:
            self._write_attributes(node)
        elif node.type == OTBMNodeType.OTBM_TILE_AREA:
            self._write_tile_area(node)
        elif node.type == OTBMNodeType.OTBM_TILE:
            self._write_tile(node)
            self._write_attributes(node)
        elif node.type == OTBMNodeType.OTBM_ITEM:
            self._write_item(node)
            self._write_attributes(node)
        elif node.type == OTBMNodeType.OTBM_TOWN:
            self._write_town(node)
        elif node.type == OTBMNodeType.OTBM_HOUSETILE:
            self._write_house_tile(node)
            self._write_attributes(node)
        elif node.type == OTBMNodeType.OTBM_WAYPOINT:
            self._write_waypoint(node)

        if node.children:
            for child in node.children:
                self._write_node(child)

        self.buffer.write_byte(0xFF)

    def _write_root_node(self, node: OTBMRootNode):
        self.buffer.escape_write_uint32_le(node.version)
        self.buffer.escape_write_uint16_le(node.width)
        self.buffer.escape_write_uint16_le(node.height)
        self.buffer.escape_write_uint32_le(node.item_major_version)
        self.buffer.escape_write_uint32_le(node.item_minor_version)

    def _write_tile_area(self, node: OTBMTileArea):
        self.buffer.escape_write_uint16_le(node.x if node.x else 0)
        self.buffer.escape_write_uint16_le(node.y if node.y else 0)
        self.buffer.escape_write_byte(node.z if node.z else 0)

    def _write_tile(self, node: OTBMTile):
        self.buffer.escape_write_byte(node.x if node.x else 0)
        self.buffer.escape_write_byte(node.y if node.y else 0)

    def _write_item(self, node: OTBMItem):
        self.buffer.escape_write_uint16_le(node.id if node.id else 0)

    def _write_town(self, node: OTBMTown):
        self.buffer.escape_write_uint32_le(node.town_id if node.town_id else 0)
        self.buffer.escape_write_string(node.name if node.name else 'No name')
        self.buffer.escape_write_uint16_le(node.x if node.x else 0)
        self.buffer.escape_write_uint16_le(node.y if node.y else 0)
        self.buffer.escape_write_byte(node.z if node.z else 0)

    def _write_house_tile(self, node: OTBMHouseTile):
        self.buffer.escape_write_byte(node.x if node.x else 0)
        self.buffer.escape_write_byte(node.y if node.y else 0)
        self.buffer.escape_write_uint32_le(node.house_id if node.house_id else 0)

    def _write_waypoint(self, node: OTBMWaypoint):
        self.buffer.escape_write_string(node.name if node.name else 'No name')
        self.buffer.escape_write_uint16_le(node.x if node.x else 0)
        self.buffer.escape_write_uint16_le(node.y if node.y else 0)
        self.buffer.escape_write_byte(node.z if node.z else 0)

    def _write_attributes(self, node: OTBMNode):
        if hasattr(node.attributes, 'sub_type'):
            self.buffer.escape_write_byte(node.attributes.sub_type)

        if hasattr(node.attributes, 'text'):
            self.buffer.write_byte(OTBMAttribute.TEXT.value)
            self.buffer.escape_write_string(node.attributes.text)

        if hasattr(node.attributes, 'spawn_file'):
            self.buffer.write_byte(OTBMAttribute.EXT_SPAWN_FILE.value)
            self.buffer.escape_write_string(node.attributes.spawn_file)

        if hasattr(node.attributes, 'house_file'):
            self.buffer.write_byte(OTBMAttribute.EXT_HOUSE_FILE.value)
            self.buffer.escape_write_string(node.attributes.house_file)

        if hasattr(node.attributes, 'house_door_id'):
            self.buffer.write_byte(OTBMAttribute.HOUSEDOORID.value)
            self.buffer.escape_write_byte(node.attributes.house_door_id)

        if hasattr(node.attributes, 'description'):
            if node.attributes.description:
                for desc in node.attributes.description:
                    self.buffer.write_byte(OTBMAttribute.DESCRIPTION.value)
                    self.buffer.escape_write_string(desc)

        if hasattr(node.attributes, 'desc'):
            self.buffer.write_byte(OTBMAttribute.DESC.value)
            self.buffer.escape_write_string(node.attributes.desc)

        if hasattr(node.attributes, 'depot_id'):
            self.buffer.write_byte(OTBMAttribute.DEPOT_ID.value)
            self.buffer.escape_write_uint16_le(node.attributes.depot_id)

        if hasattr(node.attributes, 'tile_flags'):
            self.buffer.write_byte(OTBMAttribute.TILE_FLAGS.value)
            flags = OTBMTileState.TILESTATE_NONE.value

            flags |= (1 if node.attributes.tile_flags.protection else 0) & OTBMTileState.TILESTATE_PROTECTIONZONE.value
            flags |= (1 if node.attributes.tile_flags.no_pvp else 0) & OTBMTileState.TILESTATE_NOPVP.value
            flags |= (1 if node.attributes.tile_flags.no_logout else 0) & OTBMTileState.TILESTATE_NOLOGOUT.value
            flags |= (1 if node.attributes.tile_flags.pvp_zone else 0) & OTBMTileState.TILESTATE_PVPZONE.value
            flags |= (1 if node.attributes.tile_flags.refresh else 0) & OTBMTileState.TILESTATE_REFRESH.value

            self.buffer.escape_write_uint32_le(flags)

        if hasattr(node.attributes, 'rune_charges'):
            self.buffer.write_byte(OTBMAttribute.RUNE_CHARGES.value)
            self.buffer.escape_write_byte(node.attributes.rune_charges)

        if hasattr(node.attributes, 'count'):
            self.buffer.write_byte(OTBMAttribute.COUNT.value)
            self.buffer.escape_write_byte(node.attributes.count)

        if hasattr(node.attributes, 'tile_id'):
            self.buffer.write_byte(OTBMAttribute.ITEM.value)
            self.buffer.escape_write_uint16_le(node.attributes.tile_id)

        if hasattr(node.attributes, 'action_id'):
            self.buffer.write_byte(OTBMAttribute.ACTION_ID.value)
            self.buffer.escape_write_uint16_le(node.attributes.action_id)

        if hasattr(node.attributes, 'unique_id'):
            self.buffer.write_byte(OTBMAttribute.UNIQUE_ID.value)
            self.buffer.escape_write_uint16_le(node.attributes.unique_id)

        if hasattr(node.attributes, 'destination'):
            self.buffer.write_byte(OTBMAttribute.TELE_DEST.value)
            self.buffer.escape_write_uint16_le(node.attributes.destination.x if node.attributes.destination.x else 0)
            self.buffer.escape_write_uint16_le(node.attributes.destination.y if node.attributes.destination.y else 0)
            self.buffer.escape_write_byte(node.attributes.destination.z if node.attributes.destination.z else 0)

        if hasattr(node.attributes, 'charges'):
            self.buffer.write_byte(OTBMAttribute.CHARGES.value)
            self.buffer.escape_write_uint16_le(node.attributes.charges if node.attributes.charges else 0)

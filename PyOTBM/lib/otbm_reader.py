from const import OTBMNodeType, OTBMNodeSpecialByte
from lib.bytes import Byt3s
from lib.otbm_house_tile import OTBMHouseTile
from lib.otbm_item import OTBMItem
from lib.otbm_map_data import OTBMMapData
from lib.otbm_node import OTBMNode
from lib.otbm_root_node import OTBMRootNode
from lib.otbm_tile import OTBMTile
from lib.otbm_tile_area import OTBMTileArea
from lib.otbm_town import OTBMTown
from lib.otbm_towns import OTBMTowns
from lib.otbm_waypoint import OTBMWaypoint
from lib.otbm_waypoints import OTBMWaypoints

class OTBMReader(Byt3s):

    def __init__(self, data):
        super().__init__(data)
        self._stack = []

    def parse(self):
        self.position = 0
        self._stack = []

        while self.position < self.byte_length:
            self._read_next_node()

        if len(self._stack) != 1:
            raise ValueError('Failed to parse .OTBM file.')
        else:
            return self._stack[0]

    def get_root_node(self):
        if len(self._stack) != 1:
            return self.parse()
        else:
            return self._stack[0]

    def get_map_data(self):
        if len(self._stack) != 1:
            self.parse()
        return self._stack[0].first_child

    def get_tile_areas(self):
        if len(self._stack) != 1:
            self.parse()

        tile_areas = []

        if isinstance(self._stack[0].children[0], OTBMMapData):
            for child in self._stack[0].children[0].children:
                if isinstance(child, OTBMTileArea):
                    tile_areas.append(child)
        else:
            raise ValueError('Could not locate MapData instance. (Probably due to failed .OTBM parse)')

        return tile_areas

    def get_waypoints(self):
        if len(self._stack) != 1:
            self.parse()

        if isinstance(self._stack[0].children[0], OTBMMapData):
            for child in self._stack[0].children[0].children:
                if isinstance(child, OTBMWaypoints):
                    return child.children

            return []
        else:
            raise ValueError('Could not locate MapData instance. (Probably due to failed .OTBM parse)')

    def get_towns(self):
        if len(self._stack) != 1:
            self.parse()

        if isinstance(self._stack[0].children[0], OTBMMapData):
            for child in self._stack[0].children[0].children:
                if isinstance(child, OTBMTowns):
                    return child.children

            return []
        else:
            raise ValueError('Could not locate MapData instance. (Probably due to failed .OTBM parse)')

    def get_tiles(self):
        tiles = []
        if len(self._stack) != 1:
            self.parse()

        if isinstance(self._stack[0].first_child, OTBMMapData):
            for child in self._stack[0].first_child.children:
                if isinstance(child, OTBMTileArea):
                    for tile in child.children:
                        tiles.append(tile)

        return tiles

    def get_house_tiles(self):
        return [tile for tile in self.get_tiles() if isinstance(tile, OTBMHouseTile)]


    def get_tile_at(self, x, y, z):
        tiles = self.get_tiles()
        for tile in tiles:
            if tile.real_x == x and tile.real_y == y and tile.z == z:
                return tile
        return None

    def get_top_level_items(self):
        tiles = self.get_tiles()
        items = []

        for tile in tiles:
            items.extend(tile.children)

        return items

    def _get_next_node_start_or_end_position(self):
        next_node_start_or_end_position = -1
        previous_position = self.position
        has_escaped = False

        while self.position < self.byte_length:
            byte = self.escape_read_byte()

            if (self.position - previous_position) > 1:
                has_escaped = True
            else:
                has_escaped = False

            previous_position = self.position

            if (byte == OTBMNodeSpecialByte.START.value and not has_escaped) or (byte == OTBMNodeSpecialByte.END.value and not has_escaped):
                next_node_start_or_end_position = self.position - 1
                break

        return next_node_start_or_end_position

    def _has_child(self):
        return self.peek_byte() == OTBMNodeSpecialByte.START.value

    def _has_sibling(self):
        position_save = self.position
        self.position += 1  # Skip 0xFF (If sibling)
        has_sibling = self.peek_byte() == OTBMNodeSpecialByte.START.value
        self.position = position_save
        return has_sibling

    def _traverse_up(self):
        self.read_byte()
        popped_node = self._stack.pop()
        if self._stack[-1]:
            self._stack[-1].children.append(popped_node)
        else:
            raise ValueError()

    def _read_next_node(self):
        next_node_start_position = self._get_next_node_start_or_end_position()
        next_node_end_position = self._get_next_node_start_or_end_position()

        if next_node_end_position == -1:
            # Reached the end
            self.read_byte()
            return

        self.position = next_node_start_position

        if self.peek_byte() == OTBMNodeSpecialByte.START.value:
            self.read_byte()  # Read 0xFE

            node = self._get_node_type(next_node_end_position)

            # After doing all node byte reading
            if self.position != next_node_end_position:
                raise ValueError(f'Node parse error. Current byte position ({self.position}) is not equal to node end position ({next_node_end_position}).')

            if node is not None:
                # Add ref to parent
                if self._stack:
                    node.parent = self._stack[-1]

                # Add ref to siblings
                prev_sibling = node.parent.children[-1] if node.parent else None

                if prev_sibling is not None:
                    node.prev_sibling = prev_sibling
                    # Add next sibling ref to previous sibling
                    prev_sibling.next_sibling = node

                if not self._stack or self._has_child():
                    self._stack.append(node)
                else:
                    self._stack[-1].children.append(node)
                    node_end = self.read_byte()  # Read 0xFF node end
                    if node_end != OTBMNodeSpecialByte.END.value:
                        raise ValueError('Not end byte')
        else:
            if self.peek_byte() == OTBMNodeSpecialByte.END.value:
                self._traverse_up()
            else:
                raise ValueError()

    def _get_node_type(self, node_end_position):
        type_byte = self.read_byte()

        if type_byte == OTBMNodeType.OTBM_MAP_HEADER.value:
            root_node = OTBMRootNode()
            root_node.set(self)
            return root_node
        elif type_byte == OTBMNodeType.OTBM_MAP_DATA.value:
            map_data = OTBMMapData()
            map_data.set_attributes(self, node_end_position)
            return map_data
        elif type_byte == OTBMNodeType.OTBM_TILE_AREA.value:
            tile_area = OTBMTileArea()
            tile_area.set(self)
            return tile_area
        elif type_byte == OTBMNodeType.OTBM_TILE.value:
            tile = OTBMTile()
            tile.set(self)
            tile.set_attributes(self, node_end_position)
            return tile
        elif type_byte == OTBMNodeType.OTBM_ITEM.value:
            item = OTBMItem()
            item.set(self)
            item.set_attributes(self, node_end_position)
            return item
        elif type_byte == OTBMNodeType.OTBM_TOWNS.value:
            towns = OTBMTowns()
            return towns
        elif type_byte == OTBMNodeType.OTBM_TOWN.value:
            town = OTBMTown()
            town.set(self)
            return town
        elif type_byte == OTBMNodeType.OTBM_HOUSETILE.value:
            house_tile = OTBMHouseTile()
            house_tile.set(self)
            house_tile.set_attributes(self, node_end_position)
            return house_tile
        elif type_byte == OTBMNodeType.OTBM_WAYPOINTS.value:
            waypoints = OTBMWaypoints()
            return waypoints
        elif type_byte == OTBMNodeType.OTBM_WAYPOINT.value:
            waypoint = OTBMWaypoint()
            waypoint.set(self)
            return waypoint
        else:
            print(f'Node type: {type_byte} is not supported yet.')
            return None

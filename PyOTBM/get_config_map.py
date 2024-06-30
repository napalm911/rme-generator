import json
from lib.bytes import Byt3s
from lib.otbm_root_node import OTBMRootNode
from lib.otbm_node import OTBMNodeType

def read_map_configuration(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()

    otbm_buffer = Byt3s(data)
    root_node = OTBMRootNode()
    root_node.set(otbm_buffer)
    
    # Recursively parse all nodes if needed
    # parse_nodes(root_node, otbm_buffer)

    config = {
        "version": root_node.version,
        "width": root_node.width,
        "height": root_node.height,
        "item_major_version": root_node.item_major_version,
        "item_minor_version": root_node.item_minor_version
    }
    return config

def parse_nodes(node, buffer):
    while buffer.position < len(buffer.data):
        node_type = buffer.peek_byte()

        if node_type == OTBMNodeType.OTBM_TILE.value:
            tile = OTBMTile()
            tile.set(buffer)
            parse_nodes(tile, buffer)
            node.add_child(tile)
        elif node_type == OTBMNodeType.OTBM_ITEM.value:
            item = OTBMItem()
            item.set(buffer)
            node.add_child(item)
        elif node_type == OTBMNodeType.OTBM_TILE_AREA.value:
            tile_area = OTBMTileArea()
            tile_area.set(buffer)
            parse_nodes(tile_area, buffer)
            node.add_child(tile_area)
        elif node_type == OTBMNodeType.OTBM_TOWN.value:
            town = OTBMTown()
            town.set(buffer)
            node.add_child(town)
        elif node_type == OTBMNodeType.OTBM_WAYPOINT.value:
            waypoint = OTBMWaypoint()
            waypoint.set(buffer)
            node.add_child(waypoint)
        else:
            buffer.position += 1
            break

if __name__ == "__main__":
    file_path = "/home/max/napalm911/otchaos-max/Server/data/world/Tibia74.otbm"
    config = read_map_configuration(file_path)
    print(json.dumps(config, indent=4))

import random
from lib.otbm_writer import OTBMWriter
from lib.otbm_root_node import OTBMRootNode
from lib.otbm_tile import OTBMTile
from lib.otbm_item import OTBMItem
from const import OTBMClientVersion
from get_config_map import read_map_configuration

def read_valid_item_ids(otb_file_path):
    # Implement reading of the `items.otb` file and extract valid item IDs
    # This is a placeholder implementation
    valid_item_ids = [101, 102, 103, 104, 105]  # Replace with actual reading logic
    return valid_item_ids

def generate_random_map(file_path, config, item_ids):
    root_node = OTBMRootNode()
    root_node.width = config["width"]
    root_node.height = config["height"]
    root_node.version = config["version"]
    root_node.item_major_version = 3
    root_node.item_minor_version = 3


    # Create tile areas
    for x in range(root_node.width):
        for y in range(root_node.height):
            tile = OTBMTile()
            tile.x = x
            tile.y = y

            # Randomly assign an item ID to the tile from valid item IDs
            item = OTBMItem()
            item.id = random.choice(item_ids)
            tile.add_child(item)

            root_node.add_child(tile)

    writer = OTBMWriter(root_node)
    with open(file_path, 'wb') as f:
        f.write(writer.write_buffer())

if __name__ == "__main__":
    config_path = "/home/max/napalm911/otchaos-max/Tools/PyRME/Tibia74.otbm"
    new_map_path = "/home/max/napalm911/otchaos-max/Tools/PyRME/test.otbm"
    otb_file_path = "/home/max/napalm911/otchaos-max/Tools/PyRME/items.otb"

    # Read configuration from existing map
    config = read_map_configuration(config_path)
    
    # Read valid item IDs from the `items.otb` file
    item_ids = read_valid_item_ids(otb_file_path)

    # Generate new map based on the existing map's configuration
    generate_random_map(new_map_path, config, item_ids)

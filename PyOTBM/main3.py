import random
from lib.otbm_writer import OTBMWriter
from lib.otbm_root_node import OTBMRootNode
from lib.otbm_tile import OTBMTile
from lib.otbm_item import OTBMItem
from const import OTBMClientVersion

def generate_random_map(file_path, width, height, item_ids):
    root_node = OTBMRootNode()
    root_node.width = width
    root_node.height = height
    root_node.version = 2
    root_node.item_major_version = OTBMClientVersion._760.value  # Set to Tibia 7.6 version
    root_node.item_minor_version = 0


    # Create tile areas
    for x in range(width):
        for y in range(height):
            tile = OTBMTile()
            tile.x = x
            tile.y = y

            # Randomly assign an item ID to the tile
            item = OTBMItem()
            item.id = random.choice(item_ids)
            tile.add_child(item)

            root_node.add_child(tile)

    writer = OTBMWriter(root_node)
    with open(file_path, 'wb') as f:
        f.write(writer.write_buffer())

if __name__ == "__main__":
    file_path = "/home/max/napalm911/otchaos-max/Tools/PyRME/test.otbm"
    width = 100
    height = 100
    item_ids = [101, 102, 103, 104, 105]  # Example item IDs for different terrains
    generate_random_map(file_path, width, height, item_ids)

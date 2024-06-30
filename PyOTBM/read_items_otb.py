import struct
import io

class ItemType:
    def __init__(self):
        self.id = 0
        self.clientID = 0
        self.name = ""
        self.description = ""
        self.weight = 0.0
        self.volume = 0
        self.maxTextLen = 0
        self.group = 0
        self.type = 0
        self.unpassable = False
        self.blockMissiles = False
        self.blockPathfinder = False
        self.hasElevation = False
        self.pickupable = False
        self.moveable = False
        self.stackable = False
        self.floorChangeDown = False
        self.floorChangeNorth = False
        self.floorChangeEast = False
        self.floorChangeSouth = False
        self.floorChangeWest = False
        self.floorChange = False
        self.alwaysOnBottom = False
        self.isHangable = False
        self.hookEast = False
        self.hookSouth = False
        self.allowDistRead = False
        self.rotable = False
        self.canReadText = False
        self.rotateTo = 0
        self.alwaysOnTopOrder = 0

    def __repr__(self):
        return f"ItemType(id={self.id}, clientID={self.clientID}, name={self.name}, description={self.description})"

class ItemDatabase:
    def __init__(self):
        self.items = {}
        self.maxItemId = 0

    def clear(self):
        self.items.clear()
        self.maxItemId = 0

    def load_from_otb(self, filepath):
        with open(filepath, "rb") as f:
            self._parse_otb(f)

    def _parse_otb(self, file):
        header = file.read(4)
        if header != b'OTBI':
            raise ValueError("Invalid OTB file")

        major_version, minor_version, build_number = struct.unpack('<III', file.read(12))
        self.major_version = major_version
        self.minor_version = minor_version
        self.build_number = build_number

        root_node = self._read_node(file)
        if root_node['type'] != 1:
            raise ValueError("Invalid root node type")

        item_node = root_node['child']
        while item_node:
            item = self._parse_item_node(item_node)
            self.items[item.id] = item
            if item.id > self.maxItemId:
                self.maxItemId = item.id
            item_node = item_node['next']

    def _read_node(self, file):
        node_type = struct.unpack('<B', file.read(1))[0]
        data_length = struct.unpack('<H', file.read(2))[0]
        data = file.read(data_length)
        return {
            'type': node_type,
            'data': data,
            'child': None,
            'next': None
        }

    def _parse_item_node(self, node):
        data = io.BytesIO(node['data'])
        group = struct.unpack('<B', data.read(1))[0]

        item = ItemType()
        item.group = group
        while data.tell() < len(node['data']):
            attribute, datalen = struct.unpack('<BH', data.read(3))
            if attribute == 16:  # ITEM_ATTR_SERVERID
                item.id = struct.unpack('<H', data.read(2))[0]
            elif attribute == 17:  # ITEM_ATTR_CLIENTID
                item.clientID = struct.unpack('<H', data.read(2))[0]
            elif attribute == 18:  # ITEM_ATTR_NAME
                item.name = data.read(datalen).decode('utf-8')
            elif attribute == 19:  # ITEM_ATTR_DESCR
                item.description = data.read(datalen).decode('utf-8')
            elif attribute == 20:  # ITEM_ATTR_WEIGHT
                item.weight = struct.unpack('<d', data.read(8))[0]
            elif attribute == 21:  # ITEM_ATTR_VOLUME
                item.volume = struct.unpack('<H', data.read(2))[0]
            elif attribute == 22:  # ITEM_ATTR_ROTATETO
                item.rotateTo = struct.unpack('<H', data.read(2))[0]
            elif attribute == 23:  # ITEM_ATTR_MAXITEMS
                item.maxTextLen = struct.unpack('<H', data.read(2))[0]
            # Add other attributes as necessary...

        return item

def main():
    db = ItemDatabase()
    db.load_from_otb("/home/max/napalm911/otchaos-max/Tools/PyOTBM/items.otb")

    for item_id, item in db.items.items():
        print(item)

if __name__ == "__main__":
    main()

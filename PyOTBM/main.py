from lib.bytes import Byt3s
from lib.otbm_root_node import OTBMRootNode

def read_otbm_file(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()

    otbm_buffer = Byt3s(data)
    root_node = OTBMRootNode()
    root_node.set(otbm_buffer)
    
    return root_node.as_raw_object()

if __name__ == "__main__":
    file_path = "/home/max/napalm911/otchaos-max/Tools/PyRME/Tibia74.otbm"
    map_data = read_otbm_file(file_path)
    print(map_data)

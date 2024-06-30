#include <wx/wx.h>
#include <pugixml.hpp>
#include "client_version.h"
#include "iomap_otbm.h"
#include "map.h"
#include "tile.h"
#include "item.h"
#include <wx/filename.h>


// Function to initialize client version
void initializeClientVersion(const std::string& clientDir) {
    ClientVersion clientVersion;
    clientVersion.setClientPath(clientDir);
}

// Function to create and save a new map
void createMap(const std::string& outputFilePath) {
    Map map;
    map.createEmptyMap(100, 100); // Create a 100x100 empty map
    
    // Fill map with items
    for (int x = 0; x < 100; ++x) {
        for (int y = 0; y < 100; ++y) {
            Tile* tile = map.getTile(x, y);
            if (!tile) {
                tile = map.createTile(x, y);
            }
            
            Item* item = Item::CreateItem(1234); // Replace 1234 with your item ID
            tile->addItem(item);
        }
    }
    
    // Save the map
    IOMapOTBM ioMap;
    ioMap.saveMap(&map, outputFilePath);
}

int main() {
    std::string clientDir = "/Users/maxramirez/Downloads/otchaos-client (localhost)/data/things/772"; // Path to Tibia client directory
    std::string outputFilePath = "/Users/maxramirez/Documents/GitHub/otchaos-max/Tools/RME-Gen/output/map.otbm"; // Path to save the generated map

    initializeClientVersion(clientDir);
    createMap(outputFilePath);

    return 0;
}
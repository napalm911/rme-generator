cmake_minimum_required(VERSION 3.15)
project(rme_map_generator)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Add vcpkg toolchain
if(DEFINED ENV{VCPKG_ROOT})
    set(CMAKE_TOOLCHAIN_FILE "$ENV{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake" CACHE STRING "")
endif()

# Find wxWidgets
find_package(wxWidgets CONFIG REQUIRED)

# Find pugixml
find_package(pugixml CONFIG REQUIRED)

# Add source files
set(SOURCES
    main.cpp
    client_version.cpp
    iomap_otbm.cpp
    map.cpp
    tile.cpp
    item.cpp
)

# Add executable
add_executable(${PROJECT_NAME} ${SOURCES})

# Link libraries
target_link_libraries(${PROJECT_NAME} PRIVATE wx::core wx::base pugixml::pugixml)

# Include directories
target_include_directories(${PROJECT_NAME} PRIVATE ${wxWidgets_INCLUDE_DIRS})
cmake_minimum_required(VERSION 3.10)
project(rplidar_sdk)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add source files
set(SDK_SOURCES
    "src/rplidar_driver.cpp"
    "src/hal/thread.cpp"
    "src/arch/win32/net_serial.cpp"
    "src/arch/win32/timer.cpp"
)

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

# Create static library
add_library(rplidar_sdk STATIC ${SDK_SOURCES})

# Set output directories
set_target_properties(rplidar_sdk PROPERTIES
    ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/lib"
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/lib"
)

# Windows-specific settings
if(WIN32)
    target_compile_definitions(rplidar_sdk PRIVATE 
        _USE_MATH_DEFINES
        _WIN32
    )
endif() 
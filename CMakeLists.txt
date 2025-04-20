cmake_minimum_required(VERSION 3.10)
project(hairdresser_robot)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Python
find_package(Python COMPONENTS Interpreter Development REQUIRED)

# Add pybind11 as a subdirectory
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/pybind11)

# RPLIDAR SDK 경로 설정
set(RPLIDAR_SDK_PATH "${CMAKE_CURRENT_SOURCE_DIR}/rplidar_sdk-master/sdk")

# SDK 소스 파일 추가
set(RPLIDAR_SOURCES
    "${RPLIDAR_SDK_PATH}/src/rplidar_driver.cpp"
    "${RPLIDAR_SDK_PATH}/src/sl_lidar_driver.cpp"
    "${RPLIDAR_SDK_PATH}/src/sl_serial_channel.cpp"
    "${RPLIDAR_SDK_PATH}/src/sl_tcp_channel.cpp"
    "${RPLIDAR_SDK_PATH}/src/sl_udp_channel.cpp"
    "${RPLIDAR_SDK_PATH}/src/sl_crc.cpp"
    "${RPLIDAR_SDK_PATH}/src/sl_async_transceiver.cpp"
    "${RPLIDAR_SDK_PATH}/src/sl_lidarprotocol_codec.cpp"
    "${RPLIDAR_SDK_PATH}/src/arch/win32/net_serial.cpp"
    "${RPLIDAR_SDK_PATH}/src/arch/win32/timer.cpp"
    "${RPLIDAR_SDK_PATH}/src/hal/thread.cpp"
    "${RPLIDAR_SDK_PATH}/src/dataunpacker/dataunpacker.cpp"
    "${RPLIDAR_SDK_PATH}/src/dataunpacker/unpacker/handler_capsules.cpp"
    "${RPLIDAR_SDK_PATH}/src/dataunpacker/unpacker/handler_hqnode.cpp"
    "${RPLIDAR_SDK_PATH}/src/dataunpacker/unpacker/handler_normalnode.cpp"
    "${RPLIDAR_SDK_PATH}/src/arch/win32/net_socket.cpp"
)

# Include directories
include_directories(
    ${Python_INCLUDE_DIRS}
    "${RPLIDAR_SDK_PATH}/include"
    "${RPLIDAR_SDK_PATH}/src"
    "${RPLIDAR_SDK_PATH}/src/dataunpacker"
    "${RPLIDAR_SDK_PATH}/src/dataunpacker/unpacker"
    "${RPLIDAR_SDK_PATH}/src/hal"
    "${RPLIDAR_SDK_PATH}/src/arch/win32"
)

# Add the library
pybind11_add_module(lidar_interface 
    lidar_interface.cpp
    ${RPLIDAR_SOURCES}
)

# Windows-specific settings
if(WIN32)
    target_compile_definitions(lidar_interface PRIVATE 
        _USE_MATH_DEFINES
        _WIN32
    )
endif()

# Link libraries
target_link_libraries(lidar_interface PRIVATE
    ${Python_LIBRARIES}
)

# Install the module
install(TARGETS lidar_interface
    LIBRARY DESTINATION ${Python_SITEARCH}
) 
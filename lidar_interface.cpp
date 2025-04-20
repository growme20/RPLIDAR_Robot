#include <iostream>
#include <vector>
#include <cmath>
#include <rplidar.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

class LidarInterface {
private:
    rp::standalone::rplidar::RPlidarDriver* driver;
    bool is_connected;
    
public:
    LidarInterface() : driver(nullptr), is_connected(false) {}
    
    ~LidarInterface() {
        disconnect();
    }
    
    bool connect(const std::string& port) {
        // RPLIDAR 드라이버 생성
        driver = rp::standalone::rplidar::RPlidarDriver::CreateDriver();
        if (!driver) {
            std::cout << "Failed to create RPLIDAR driver" << std::endl;
            return false;
        }

        // RPLIDAR 연결
        if (IS_FAIL(driver->connect(port.c_str(), 115200))) {
            std::cout << "Failed to connect to RPLIDAR at " << port << std::endl;
            rp::standalone::rplidar::RPlidarDriver::DisposeDriver(driver);
            driver = nullptr;
            return false;
        }

        // RPLIDAR 상태 확인
        rplidar_response_device_info_t deviceInfo;
        if (IS_FAIL(driver->getDeviceInfo(deviceInfo))) {
            std::cout << "Failed to get RPLIDAR device info" << std::endl;
            disconnect();
            return false;
        }

        is_connected = true;
        std::cout << "Successfully connected to RPLIDAR" << std::endl;
        return true;
    }
    
    void disconnect() {
        if (driver) {
            stopMotor();
            driver->disconnect();
            rp::standalone::rplidar::RPlidarDriver::DisposeDriver(driver);
            driver = nullptr;
        }
        is_connected = false;
    }
    
    bool startMotor() {
        if (!driver || !is_connected) return false;
        
        // 모터 시작
        driver->startMotor();
        
        // 스캔 시작
        if (IS_FAIL(driver->startScan(false, true))) {
            std::cout << "Failed to start RPLIDAR scan" << std::endl;
            return false;
        }
        
        return true;
    }
    
    bool stopMotor() {
        if (!driver || !is_connected) return false;
        driver->stop();
        driver->stopMotor();
        return true;
    }
    
    std::vector<std::tuple<float, float, float>> getScanData() {
        std::vector<std::tuple<float, float, float>> scan_data;
        
        if (!driver || !is_connected) return scan_data;
        
        rplidar_response_measurement_node_hq_t nodes[8192];
        size_t count = sizeof(nodes) / sizeof(nodes[0]);
        
        if (IS_FAIL(driver->grabScanDataHq(nodes, count))) {
            return scan_data;
        }
        
        driver->ascendScanData(nodes, count);
        
        for (size_t i = 0; i < count; ++i) {
            float quality = nodes[i].quality;
            float angle = nodes[i].angle_z_q14 * 90.f / (1 << 14);
            float distance = nodes[i].dist_mm_q2 / 4.0f;
            
            if (quality > 0 && distance > 0) {
                scan_data.emplace_back(quality, angle, distance);
            }
        }
        
        return scan_data;
    }
    
    void flushInput() {
        if (driver) {
            driver->clearNetSerialRxCache();
        }
    }
};

PYBIND11_MODULE(lidar_interface, m) {
    py::class_<LidarInterface>(m, "LidarInterface")
        .def(py::init<>())
        .def("connect", &LidarInterface::connect)
        .def("disconnect", &LidarInterface::disconnect)
        .def("startMotor", &LidarInterface::startMotor)
        .def("stopMotor", &LidarInterface::stopMotor)
        .def("getScanData", &LidarInterface::getScanData)
        .def("flushInput", &LidarInterface::flushInput);
} 
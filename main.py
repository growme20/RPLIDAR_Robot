import time
from lidar_interface import LidarInterface
from lidar_visualization import LidarVisualization
from lidar_processor import LidarProcessor

class RobotController:
    def __init__(self, port='COM5'):
        self.lidar = LidarInterface()
        self.visualization = LidarVisualization()
        self.processor = LidarProcessor()
        self.is_running = False
        self.robot_position = (0, 0)
        self.robot_angle = 0
        self.port = port
        
    def start(self):
        """시작"""
        try:
            if not self.lidar.connect(self.port):
                raise Exception("Failed to connect to LIDAR")
            
            if not self.lidar.startMotor():
                raise Exception("Failed to start LIDAR motor")
            
            self.is_running = True
            
            print("\nRobot Cleaner Simulation Started...")
            print("Close the window to exit.")
            
            self.run()
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """정지"""
        self.is_running = False
        self.lidar.stopMotor()
        self.lidar.disconnect()
        self.visualization.close()
        print("Simulation Ended")
    
    def run(self):
        """실행"""
        scan_count = 0
        last_update_time = time.time()
        update_interval = 0.1  # 100ms로 변경
        
        while self.is_running:
            try:
                scan = self.lidar.getScanData()
                if not scan:
                    time.sleep(0.01)  # 데이터가 없을 때 대기
                    continue
                
                current_time = time.time()
                if current_time - last_update_time >= update_interval:
                    # 스캔 데이터 처리
                    points = self.processor.process_scan_data(scan)
                    if points is not None:
                        # 물체 인식
                        objects = self.processor.detect_objects(points)
                        
                        # 시각화 업데이트
                        self.visualization.update_robot_position(self.robot_position, self.robot_angle)
                        self.visualization.update_scan_points(points)
                        self.visualization.update_objects(objects)
                        self.visualization.update_plot()
                    
                    last_update_time = current_time
                else:
                    time.sleep(0.01)  # 업데이트 간격 대기
                
                # 버퍼 관리
                scan_count += 1
                if scan_count % 3 == 0:
                    self.lidar.flushInput()
                    
            except Exception as e:
                print(f"Runtime Error: {e}")
                break

if __name__ == "__main__":
    robot = RobotController()
    robot.start() 
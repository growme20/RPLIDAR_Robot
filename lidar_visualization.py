import matplotlib.pyplot as plt
import numpy as np
from lidar_processor import LidarProcessor
from matplotlib import cm

class LidarVisualization:
    def __init__(self):
        # 한글 폰트 설정
        plt.rcParams['font.family'] = 'Malgun Gothic'
        
        # 그래프 초기화
        self.fig = plt.figure(figsize=(12, 8))
        
        # 메인 LIDAR 스캔 플롯 (극좌표계)
        self.ax_polar = self.fig.add_subplot(121, projection='polar')
        self.ax_polar.set_title('LIDAR 스캔 (극좌표계)')
        self.ax_polar.set_theta_zero_location('N')  # 북쪽이 0도
        self.ax_polar.set_theta_direction(-1)  # 시계 방향
        self.ax_polar.set_rlim(0, 2000)  # 최대 2m까지 표시
        
        # 직교좌표계 플롯
        self.ax_cart = self.fig.add_subplot(122)
        self.ax_cart.set_title('LIDAR 스캔 (직교좌표계)')
        self.ax_cart.set_xlim(-2000, 2000)
        self.ax_cart.set_ylim(-2000, 2000)
        self.ax_cart.grid(True)
        self.ax_cart.set_aspect('equal')
        
        # 컬러맵 설정
        self.colormap = cm.viridis
        
        # 로봇 표시용 원
        self.robot_circle = plt.Circle((0, 0), 100, color='red', alpha=0.8)
        self.ax_cart.add_patch(self.robot_circle)
        
        # 방향 표시용 화살표
        self.robot_arrow = self.ax_cart.arrow(0, 0, 0, 200, 
            head_width=40, head_length=60, fc='yellow', ec='yellow')
        
        # 스캔 데이터 시각화 요소
        self.scan_line = None
        self.scan_points = None
        self.scan_fill = None
        
        # 물체 표시용 요소들
        self.object_patches = []
        
        # 데이터 처리기 초기화
        self.processor = LidarProcessor()
        
        # 그래프 스타일 설정
        self.fig.patch.set_facecolor('black')
        self.ax_polar.set_facecolor('black')
        self.ax_cart.set_facecolor('black')
        
        # 그리드 스타일
        self.ax_polar.grid(color='gray', alpha=0.3)
        self.ax_cart.grid(color='gray', alpha=0.3)
        
        # 레이블 색상
        self.ax_polar.tick_params(colors='white')
        self.ax_cart.tick_params(colors='white')
        for spine in self.ax_polar.spines.values():
            spine.set_color('white')
        for spine in self.ax_cart.spines.values():
            spine.set_color('white')
            
        # 제목 색상
        self.ax_polar.title.set_color('white')
        self.ax_cart.title.set_color('white')
        
        # 그래프 표시
        plt.show(block=False)
        
    def update_robot_position(self, position, angle):
        """로봇 위치와 방향 업데이트"""
        self.robot_circle.center = position
        
        # 로봇 방향 업데이트
        self.robot_arrow.remove()
        angle_rad = (angle + 90) * np.pi / 180.0
        self.robot_arrow = self.ax_cart.arrow(
            position[0], position[1],
            200 * np.cos(angle_rad), 200 * np.sin(angle_rad),
            head_width=40, head_length=60, fc='yellow', ec='yellow'
        )
        
    def update_scan_points(self, points):
        """스캔 포인트 업데이트"""
        if points is None or len(points) == 0:
            return
            
        # 데이터 준비
        x = points[:, 0]
        y = points[:, 1]
        distances = np.sqrt(x**2 + y**2)
        angles = np.arctan2(y, x)
        
        # 극좌표계 업데이트
        if self.scan_line is not None:
            self.scan_line.remove()
        if self.scan_fill is not None:
            self.scan_fill.remove()
            
        # 컬러맵 적용
        colors = self.colormap(distances / np.max(distances))
        
        # 극좌표계에 데이터 표시
        self.scan_line = self.ax_polar.plot(angles, distances, 
            color='cyan', alpha=0.6, linewidth=2)[0]
        self.scan_fill = self.ax_polar.fill_between(angles, 0, distances, 
            alpha=0.2, color='cyan')
            
        # 직교좌표계 업데이트
        if self.scan_points is not None:
            self.scan_points.remove()
        self.scan_points = self.ax_cart.scatter(x, y, 
            c=distances, cmap=self.colormap, 
            s=10, alpha=0.6)
            
    def update_objects(self, objects):
        """물체 표시 업데이트"""
        # 기존 물체 표시 제거
        for patch in self.object_patches:
            patch.remove()
        self.object_patches.clear()
        
        # 새로운 물체 표시
        for center, size, angle in objects:
            # 물체 표시 원 추가
            circle = plt.Circle((center[0], center[1]), 
                size/2, color='red', alpha=0.3)
            self.ax_cart.add_patch(circle)
            self.object_patches.append(circle)
            
            # 물체 중심점 표시
            center_point = plt.Circle((center[0], center[1]), 
                10, color='yellow', alpha=0.8)
            self.ax_cart.add_patch(center_point)
            self.object_patches.append(center_point)
            
            # 텍스트 추가
            text = self.ax_cart.text(center[0], center[1], 
                f'{size:.0f}mm\n{angle:.0f}°',
                color='white', ha='center', va='center',
                fontsize=8, weight='bold',
                bbox=dict(facecolor='black', alpha=0.7,
                         edgecolor='white', pad=2))
            self.object_patches.append(text)
            
    def update_plot(self):
        """그래프 업데이트"""
        try:
            plt.pause(0.001)
        except Exception as e:
            print(f"Plot Update Error: {e}")
            
    def close(self):
        """시각화 종료"""
        plt.close(self.fig) 
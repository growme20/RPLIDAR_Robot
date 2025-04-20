import numpy as np
from collections import deque

class LidarProcessor:
    def __init__(self, buffer_size=200):
        self.map_data = deque(maxlen=buffer_size)
        self.cluster_threshold = 200  # mm
        self.min_points_for_object = 3
        
    def detect_objects(self, points):
        """물체 인식"""
        if len(points) < self.min_points_for_object:
            return []
            
        # 점들 간의 거리 계산
        distances = np.zeros((len(points), len(points)))
        for i in range(len(points)):
            for j in range(i+1, len(points)):
                distances[i,j] = distances[j,i] = np.sqrt(np.sum((points[i] - points[j])**2))
        
        # 클러스터링
        clusters = []
        used = set()
        
        for i in range(len(points)):
            if i in used:
                continue
                
            cluster = [i]
            used.add(i)
            
            for j in range(len(points)):
                if j not in used and distances[i,j] < self.cluster_threshold:
                    cluster.append(j)
                    used.add(j)
            
            if len(cluster) >= self.min_points_for_object:
                clusters.append(cluster)
        
        # 각 클러스터의 중심점과 크기 계산
        objects = []
        for cluster in clusters:
            cluster_points = points[cluster]
            center = np.mean(cluster_points, axis=0)
            size = np.max(distances[cluster][:, cluster])
            
            angle = np.arctan2(center[1], center[0]) * 180 / np.pi
            if angle < 0:
                angle += 360
                
            objects.append((center, size, angle))
            
        return objects
        
    def process_scan_data(self, scan):
        """스캔 데이터 처리"""
        x_points = []
        y_points = []
        
        for i, (quality, angle, distance) in enumerate(scan):
            if i % 4 == 0:  # 샘플링
                if distance > 0 and quality > 0:
                    angle_rad = (angle + 90) * np.pi / 180.0
                    x = distance * np.cos(angle_rad)
                    y = distance * np.sin(angle_rad)
                    x_points.append(x)
                    y_points.append(y)
        
        return np.column_stack((x_points, y_points)) if x_points and y_points else None 
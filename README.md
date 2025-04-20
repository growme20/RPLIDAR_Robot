# RPLIDAR 로봇 청소기 시뮬레이션

이 프로젝트는 RPLIDAR A1을 사용하여 로봇 청소기의 환경 인식 시스템을 구현한 것입니다. LIDAR 센서로부터 실시간으로 거리 데이터를 수집하고, 이를 시각화하여 보여줍니다.

## 주요 기능

- RPLIDAR A1 센서 실시간 데이터 수집
- 극좌표계와 직교좌표계를 이용한 듀얼 뷰 시각화
- 물체 감지 및 거리 측정
- 실시간 데이터 처리 및 표시

## 시스템 요구사항

- Python 3.8 이상
- C++ 컴파일러 (MSVC, GCC, 등)
- CMake 3.8 이상
- RPLIDAR SDK
- 필요한 Python 패키지:
  - numpy
  - matplotlib
  - pybind11

## 설치 방법

1. 저장소 클론
```bash
git clone https://github.com/[사용자명]/[저장소명].git
cd [저장소명]
```

2. CMake 빌드
```bash
mkdir build
cd build
cmake ..
cmake --build . --config Release
cd ..
```

3. Python 모듈 복사
```bash
copy "build/Release/lidar_interface.cp312-win_amd64.pyd" .
```

## 실행 방법

1. RPLIDAR A1을 컴퓨터에 연결합니다.
2. 다음 명령어로 프로그램을 실행합니다:
```bash
python main.py
```

## 시각화 설명

- 왼쪽 화면 (극좌표계):
  - 로봇을 중심으로 한 360도 스캔 데이터
  - 거리는 중심에서부터의 mm 단위
  - 청록색 영역은 감지된 물체를 나타냄

- 오른쪽 화면 (직교좌표계):
  - X-Y 평면에 표시된 스캔 데이터
  - 빨간 원은 로봇의 현재 위치
  - 노란색 화살표는 로봇의 방향
  - 흰색 박스는 감지된 물체의 거리와 각도 정보

## 라이센스

이 프로젝트는 MIT 라이센스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요. 
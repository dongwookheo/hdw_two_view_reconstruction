# hdw_two_view_reconstruction
- 3D reconstruction 을 위한 레포지토리
- 예제 이미지는 Oxford university의 multi-view data/Wadham College dataset 중 3번, 5번 이미지를 사용하였습니다.
- **Camera matrix *K*** 와 **distortion coefficient**는 사전에 주어졌다고 가정하였습니다.
- Correspondence 문제가 해결되었다고 가정하고, 최적화 문제 이전까지의 과정을 진행하였습니다.
- 아래의 절차 순으로 진행하였습니다.
  1. Keypoints 쌍과 ***K***, **distortion coefficient**를 이용하여 **Essential matrix *E***, **Relative camera pose *R, t*** 를 계산합니다.
  2. Keypoints 쌍을 normalized image plane으로 변환합니다.
  3. ***R, t*** 를 이용하여 world coordinate에서 normalized image plane으로의 **projection matrix *P*** 를 계산합니다.
  4. ***P*** 와 normalized image plane으로 변환된 keypoints를 이용하여 **3D points**를 계산합니다.

## Results
### 1. 2D point visualization on two images
![result1](/resource/result1.png)
### 2. The essential matrix *E* between two images
![result2](/resource/result3.png)
### 3. The rotation and translation, *R* and *t*
![result3](/resource/result4.png)
### 4. 3D visualization of reconstructed 3D points in two viewpoints
![result4](/resource/result2_upsize.png)
- Points의 크기를 10으로 설정한 이미지입니다.

## Discussion
- Open3D를 통한 point cloud의 시각화 결과, 좌측 창문들에 해당하는 부분이 수평하지 못하게 복원된 것을 확인할 수 있습니다.  
  - Correspondence 문제가 해결되었다고 가정할 때, ***E***, ***R, t*** 계산 과정에서의 오류도 물론 있겠지만, triangulation 과정에서의 오류가 더 큰 것으로 보입니다.

## Todo
- [ ] Feature matching 부터 reprojection error를 최소화하는 과정까지 진행해보기

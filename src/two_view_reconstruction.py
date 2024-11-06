import copy
import numpy as np
import cv2
import utils

K = np.array([[1086, 0, 512], [0, 1086, 384], [0, 0, 1]])
DISTORTION_COEFFICIENT = np.array([-0.0568965, 0, 0, 0, 0])
MATCHING_RESULT = True
ESSENTIAL_MATRIX_RESULT = True
ROTATION_TRANSLATION_RESULT = True
RECONSTRUCTION_TO_O3D = True

if __name__ == "__main__":
    # data 폴더 내 csv 파일(2D image points)을 읽어 list로 저장
    keypoints1 = np.array(utils.get_points_from_csv("data/003.csv"))
    keypoints2 = np.array(utils.get_points_from_csv("data/005.csv"))

    # 두 이미지를 horizontal 방향으로 붙여서 시각화
    img1 = cv2.imread("data/003.jpg")
    img2 = cv2.imread("data/005.jpg")
    img = np.hstack((img1, img2))
    img1_width = img1.shape[1]
    img1_height = img1.shape[0]

    # 2D image points를 매칭 (descriptor를 고려하지 않고, 순서에 따라 매칭이 이루어진다고 가정)
    copied_keypoints2 = copy.deepcopy(keypoints2)
    for k1, k2 in zip(keypoints1, copied_keypoints2):
        k2[0] += img1_width

        # 랜덤한 색깔로 매칭된 점을 연결
        color = tuple(np.random.randint(0, 255, 3).tolist())
        cv2.line(img, k1, k2, color, 2)
        cv2.circle(img, k1, 5, color, 1)
        cv2.circle(img, k2, 5, color, 1)
    if MATCHING_RESULT:
        cv2.imshow("Image", img)
        cv2.waitKey(0)

    # Essential matrix, R, t 계산
    ret, E, R, t, mask = cv2.recoverPose(
        keypoints1.astype(np.float32),
        keypoints2.astype(np.float32),
        K,
        DISTORTION_COEFFICIENT,
        K,
        DISTORTION_COEFFICIENT,
        method=0,
    )
    if ROTATION_TRANSLATION_RESULT:
        print("* Essential matrix:", E, sep="\n")
        print("* Rotation matrix:", R, sep="\n")
        print("* Translation vector:", t, sep="\n")

    # 3D reconstruction (triangulation) in normalized image plane
    normalized_keypoints1 = cv2.undistortPoints(
        keypoints1.astype(np.float32), K, DISTORTION_COEFFICIENT
    ).reshape(-1, 2)
    normalized_keypoints2 = cv2.undistortPoints(
        keypoints2.astype(np.float32), K, DISTORTION_COEFFICIENT
    ).reshape(-1, 2)
    P1 = np.eye(3, 4, dtype=np.float32)
    P2 = np.hstack((R, t))
    #! cv::triangulatePoints(): 모든 arguments는 float type으로 넣어주어야 한다.
    X = cv2.triangulatePoints(P1, P2, normalized_keypoints1.T, normalized_keypoints2.T)
    X /= X[3]
    X = X[:3].T

    print("* 3D points:", X, sep="\n", end="\n\n")

    if RECONSTRUCTION_TO_O3D:
        import open3d as o3d

        # 3D reconstruction 결과 시각화 (Open3D)
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(X)
        vis = o3d.visualization.Visualizer()
        vis.create_window()
        vis.add_geometry(pcd)
        opt = vis.get_render_option()
        opt.point_size = 10.0  # Increase the point size
        vis.run()
        vis.destroy_window()
    else:
        import matplotlib.pyplot as plt

        # 3D reconstruction 결과 시각화 (Matplotlib)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        print(X)
        ax.scatter(X[:, 0], X[:, 1], X[:, 2])
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        plt.show()

# 入力が回転角度

import sys
import cv2
import numpy as np

import rotation_matrix as R

#コマンドライン引数の受け取り
print("--------------------------------")
value = sys.argv
path_omni_img = value[1]
theta_eye = float(value[2])
phi_eye = float(value[3])
psi_eye = float(value[4])
print("視線回転角度")
print("水平θ, 垂直φ, 光軸ψ")
print("({}, {}, {})\n".format(round(theta_eye, 1), round(phi_eye, 1), round(psi_eye, 1)))

for i in range(5, len(value), 3):
    if value[i] == "size":
        persp_width = int(value[i+1])
        persp_height = int(value[i+2])
    elif value[i] == "angle":
        horizontal_fov = float(value[i+1])
        vertical_fov = float(value[i+2])

# 全方位画像の読み込み
omni_img = cv2.imread(path_omni_img)
height_omni, width_omni, channels = omni_img.shape[:3]
print("全方位画像のサイズ")
print("width, height")
print("({}, {})\n".format(width_omni, height_omni))

# 透視投影画像サイズの計算
if not("persp_width" in locals()):
    persp_width = int(2 * np.tan(np.radians(horizontal_fov / 2)) * (width_omni / (2 * np.pi)))
    persp_height = int(2 * np.tan(np.radians(vertical_fov / 2)) * (height_omni / np.pi))
print("透視投影画像のサイズ")
print("width, height")
print("({}, {})\n".format(persp_width, persp_height))

# 画角計算
if not("horizontal_fov" in locals()):
    horizontal_fov = np.degrees(2 * np.arctan2(np.pi * persp_width, width_omni))
    vertical_fov = np.degrees(2 * np.arctan2(np.pi * persp_height, (2 * height_omni)))
print("透視投影画像の画角")
print("horizontal, vertical")
print("({}, {})\n".format(round(horizontal_fov, 1), round(vertical_fov, 1)))

# 画素間の長さ
x_pixel = 2 * np.tan(np.radians(horizontal_fov / 2)) / persp_width
y_pixel = 2 * np.tan(np.radians(vertical_fov / 2)) / persp_height

# 水平垂直回転行列
vector_v = np.array([[0], [0], [1]], np.float64)
rotation_matrix_tp = np.dot(R.theta(theta_eye), R.phi(phi_eye))

# 垂直回転行列
vector_l = np.dot(rotation_matrix_tp, vector_v)
rotation_matrix_psi = R.psi(vector_l, psi_eye)

# 視線ベクトル
vector_x = np.array([[1], [1], [1]], np.float64)

# 透視投影画像の仮作成
size_persp_img = (persp_height, persp_width, 3)
persp_img = np.zeros(size_persp_img, np.int64)

for j in range(persp_height):
    for i in range(persp_width):
        # 画像中心の座標系に変更
        vector_x[0, 0] = (i - persp_width / 2) * x_pixel
        vector_x[1, 0] = (j - persp_height / 2) * y_pixel
        # 回転
        vector_x_dash = np.dot(rotation_matrix_tp, vector_x)
        vector_x_dash = np.dot(rotation_matrix_psi, vector_x_dash)
        # 角度計算
        theta = np.arctan2(vector_x_dash[0, 0], vector_x_dash[2, 0])
        phi = -np.arctan2(vector_x_dash[1, 0], np.sqrt(np.square(vector_x_dash[0, 0]) + np.square(vector_x_dash[2, 0])))
        # 全方位画像の座標系変換
        u = (theta + np.pi) * (width_omni / (2 * np.pi))
        v = (np.pi / 2 - phi) * (height_omni / np.pi)
        # 透視投影にコピー
        persp_img[j, i] = omni_img[int(v)-1, int(u)-1]
        
# 透視投影画像の書き込み
'''
path = path_omni_img.rsplit("/", 1)
if path[0] == path_omni_img:
    path_persp_img = "({}_{}_{})_({}_{})_persp.jpg".format(theta_eye, phi_eye, psi_eye, round(horizontal_fov, 1), round(vertical_fov, 1))
else:     
    path_persp_img = path[0] + "/({}_{}_{})_({}_{})_persp.jpg".format(theta_eye, phi_eye, psi_eye, round(horizontal_fov, 1), round(vertical_fov, 1))
'''

path_persp_img = "output/({}_{}_{})_({}_{})_persp.jpg".format(theta_eye, phi_eye, psi_eye, round(horizontal_fov, 1), round(vertical_fov, 1))
cv2.imwrite(path_persp_img, persp_img)
print(path_persp_img + "を保存しました")
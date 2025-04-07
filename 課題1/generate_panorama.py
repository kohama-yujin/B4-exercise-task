import sys
import pandas as pd
import cv2
import numpy as np

import directory as dir
import coords
import homography as homo

# コマンドライン引数
value = sys.argv

# CSVファイルの読み込み
data = pd.read_csv(value[1], header=None)

# 画像1枚目の読み込み
'''
print('射影変換する画像を選択してください')
source_img_filepath = directory.run()
'''
source_img_filepath = data.iloc[0, 1]
source_img = cv2.imread(source_img_filepath)

# 画像2枚目の読み込み
'''
print('射影変換の対象となる画像を選択してください')
target_img_filepath = directory.run()
'''
target_img_filepath = data.iloc[1, 1]
target_img = cv2.imread(target_img_filepath)

# 画像情報の取得
height2, width2, channels = source_img.shape[:3]
height1, width1, channels = target_img.shape[:3]
print("第1画像サイズ 第2画像サイズ")
print("width, height width, height")
print("({}, {}) ({}, {})".format(width1, height1, width2, height2))

# 画像のサイズをリサイズ
ratio = 1
'''
while (1000 < width1 and 1000 < height1) and (1000 < width2 and 1000 < height2):
    ratio *= 2
    width1 //= 2
    height1 //= 2
    width2 //= 2
    height2 //= 2
    print("({}, {}) ({}, {})".format(width1, height1, width2, height2))
'''
if ratio == 1:
    print()
else:
    source_img = cv2.resize(source_img, (width2, height2))
    target_img = cv2.resize(target_img, (width1, height1))
    print("画像サイズが大きいため、1/{}にリサイズしました\n".format(ratio))

# 座標の格納
x_source = []
y_source = []
x_target = []
y_target = []
'''
print("いくつの座標をチェックしますか？")
coords_num = int(input())
source_points = coords.run(source_img_filepath, coords_num)
target_points = coords.run(target_img_filepath, coords_num)
for i in range(4):
    x_source.append(source_points[i][1])
    y_source.append(source_points[i][0])
    x_target.append(target_points[i][1])
    y_target.append(target_points[i][0])
'''
for i in range(1, 5):
    x_source.append(int(data.iloc[4, i])//ratio)
    y_source.append(int(data.iloc[5, i])//ratio)
    x_target.append(int(data.iloc[6, i])//ratio)
    y_target.append(int(data.iloc[7, i])//ratio)

# 射影変換行列の導出
H = homo.matrix(x_source, y_source, x_target, y_target)
Hinv = np.linalg.inv(H) 

'''パノラマ画像の生成'''
panoramasize_height = []
panoramasize_width = []

# 第1画像の4隅
panoramasize_height.append(0)
panoramasize_height.append(height1-1)
panoramasize_width.append(0)
panoramasize_width.append(width1-1)

# 第2画像射影変換後の4隅
for i in range(0, height2, height2-1):
    for j in range(0, width2, width2-1):
        x, y = homo.trans(i, j, H)
        panoramasize_height.append(x)
        panoramasize_width.append(y)

# パノラマ画像の4隅
panorama_height_min = int(np.min(panoramasize_height))
panorama_height_max = int(np.max(panoramasize_height))
panorama_width_min = int(np.min(panoramasize_width))
panorama_width_max = int(np.max(panoramasize_width))

# パノラマ画像の仮作成
panorama_size = (panorama_height_max-panorama_height_min+1, panorama_width_max-panorama_width_min+1, 3)
panorama_img = np.zeros(panorama_size, np.int64)
print("パノラマ画像サイズ")
print("width, height")
print("({}, {})\n".format(panorama_img.shape[1], panorama_img.shape[0]))

# 第1画像のコピー
for i in range(height1):
    for j in range(width1):
        panorama_img[i-panorama_height_min][j-panorama_width_min] = target_img[i][j]
print("第1画像コピー完了")

# 第2画像の射影変換
for i in range(panorama_height_min, panorama_height_max+1):
    for j in range(panorama_width_min, panorama_width_max+1):
        x_inv, y_inv = homo.inv_trans(i, j, Hinv)
        if (0 <= x_inv and x_inv < height2) and (0 <= y_inv and y_inv < width2):
            panorama_img[i-panorama_height_min][j-panorama_width_min] = source_img[int(x_inv)][int(y_inv)]
print("第2画像上書き完了")

# パノラマ画像の書き込み
#panorama_img_filepath = data.iloc[2, 1]
panorama_img_filepath = "output/panorama.jpg"

cv2.imwrite(panorama_img_filepath, panorama_img)
print("パノラマ画像完成")
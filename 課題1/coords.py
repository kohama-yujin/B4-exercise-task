import numpy as np
import cv2

# 画像の座標を表示
def run(filepath, coords_num):
	
	print("{}つの座標を選択してください".format(coords_num))
	print("  width, height")

	## マウスイベント関数
	def mouse_event(event,x,y, flags, param):
		if event == cv2.EVENT_LBUTTONUP:
			coords.append([x,y])  # 座標をリストに追加
			print(str(len(coords)) + " = " + str(x) + ", " + str(y))
			cv2.circle(img, (x,y), 1, (0,0,255), -1)  # クリックした座標に印をつける

	img = cv2.imread(filepath)  # 画像の読み込み、パスを書く
	coords = []  # 座標を格納するリストzz

	cv2.namedWindow("window", cv2.WINDOW_KEEPRATIO)  # ウィンドウを生成
	cv2.setMouseCallback("window", mouse_event)  # mouse_event 関数と関連付ける

	while True:
		cv2.imshow("window", img)  # 画像をウィンドウに表示
		print
		if  cv2.waitKey(1) & len(coords) == coords_num:
			break

	cv2.destroyAllWindows()  # すべてのウィンドウを閉じる
	print("\n")
	return coords

def main():
	run("omni.jpg", 1)

if __name__ == "__main__":
    main()
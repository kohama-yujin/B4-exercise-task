import numpy as np

'''射影変換行列の導出'''
def matrix(x, y, x_target, y_target):
  
  # 型をintからint64に変更（変えないと何故かおかしくなる）
  x = np.array(x, dtype=np.int64)
  y = np.array(y, dtype=np.int64)
  x_target = np.array(x_target, dtype=np.int64)
  y_target = np.array(y_target, dtype=np.int64)

  # Aの生成
  A = []
  for n in range(4):
     A.append([x[n], y[n], 1, 0, 0, 0, -1*x[n]*x_target[n], -1*y[n]*x_target[n]])
  for n in range(4):
     A.append([0, 0, 0, x[n], y[n], 1, -1*x[n]*y_target[n], -1*y[n]*y_target[n]])
  A = np.array(A)
  #print("A")
  #print(A) 

  # bの生成
  b = []
  for n in range(4):
     b.append([x_target[n]])
  for n in range(4):
     b.append([y_target[n]])
  b = np.array(b)
  #print("b")
  #print(b)

  # 射影変換行列の作成
  #h = np.dot(np.linalg.inv(A), b)
  h = np.dot(np.dot(np.linalg.inv(np.dot(A.T, A)), A.T), b)
  H = np.array([[h[0, 0], h[1, 0], h[2, 0]],
                [h[3, 0], h[4, 0], h[5, 0]],
                [h[6, 0], h[7, 0], 1.]])
  print("射影変換行列H")
  print(H, "\n")

  '''
  #print("h")
  #print(h)
  #print("b")
  #print(b)
  #print("Ah")
  #print(np.dot(A,h))
  '''

  return H

def trans(x, y, H):
   X1 = np.dot(H, [x, y, 1])
   x_trans = X1[0] / X1[2]
   y_trans = X1[1] / X1[2]
   
   return x_trans, y_trans

def inv_trans(x_trans, y_trans, Hinv):
   X1 = np.dot(Hinv,[x_trans, y_trans, 1])
   x = X1[0] / X1[2]
   y = X1[1] / X1[2]

   return x, y

def main():
   
   x = [250,688,668,325]
   y = [235,239,312,301]
   x_target = [112,475,454,110]
   y_target = [184,198,270,250]
   '''
   x = [1804,1864,2061,2031]
   y = [1365,1514,1308,1368]
   x_target = [1243,1293,1481,1490]
   y_target = [1385,1544,1537,1388]
   '''
   H = matrix(x,y,x_target,y_target)

   for i in range(4):
      Hinv = np.linalg.inv(H)
      x_inv, y_inv = inv_trans(x_target[i], y_target[i], Hinv)
      print("真値(", x[i], ",",  y[i], ")")
      print("計算値(", x_inv, ",",  y_inv, ")")

if __name__ == "__main__":
    main()
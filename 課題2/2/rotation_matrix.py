import numpy as np

# 水平方向の回転
def theta(theta):
    theta = np.radians(theta)
    rotate_theta = np.array([[np.cos(theta), 0, np.sin(theta)],
              [0, 1, 0],
              [-np.sin(theta), 0, np.cos(theta)]])
    #print("theta",rotate_theta)
    return rotate_theta

# 垂直方向の回転
def phi(phi):
    phi = np.radians(phi)
    rotate_phi = np.array([[1, 0, 0],
              [0, np.cos(phi), -np.sin(phi)],
              [0, np.sin(phi), np.cos(phi)]])
    #print("phi",rotate_phi)
    return rotate_phi

# 垂直方向の角度
def phi(phi):
    phi = np.radians(phi)
    rotate_phi = np.array([[1, 0, 0],
              [0, np.cos(phi), -np.sin(phi)],
              [0, np.sin(phi), np.cos(phi)]])
    #print("phi",rotate_phi)
    return rotate_phi

# 光軸方向の回転
def psi(vector_v, psi):
    psi = np.radians(psi)

    c = np.cos(psi)
    s = np.sin(psi)

    x = vector_v[0,0]
    y = vector_v[1,0]
    z = vector_v[2,0]

    w = 1 - c

    xyw = x*y*w
    yzw = y*z*w
    zxw = z*x*w
    '''
    # 反時計周り
    rotate_psi = np.array([[x**2*w + c, xyw + z*s, zxw - y*s],
                           [xyw - z*s, y**2*w + c, yzw + x*s],
                           [zxw + y*s, yzw - x*s, z**2*w + c]])
    '''
    # 時計回り
    rotate_psi = np.array([[x**2*w + c, xyw - z*s, zxw + y*s],
                           [xyw + z*s, y**2*w + c, yzw - x*s],
                           [zxw - y*s, yzw + x*s, z**2*w + c]])
    
    #print("psi",rotate_psi)
    return rotate_psi

def main():    
    vector_v = np.array([[0], [0], [1]], np.float64)
    vector_l = np.dot(phi(10), vector_v)
    print(np.dot(theta(30), vector_l))

    vector_v = np.array([[0], [0], [1]], np.float64)
    print(np.dot(np.dot(theta(30), phi(10)), vector_v))

if __name__ == "__main__":
    main()
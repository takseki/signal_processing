import numpy as np

# Kalman filter : Wikipedia に載っていた例題
# トロッコは位置 0 に静止している。
# トロッコにはランダムな 力（加速度）が与えられる。
# Δt 秒ごとにトロッコの位置 x を観測する。

# constants
dt = 0.01
F = np.array([[1, dt],
              [0, 1]])
G = np.array([dt**2/2, dt])
H = np.array([1, 0])
Sigma_a = 1.0    # ランダムに加わる加速度
Sigma_v = 0.1    # 観測誤差

# システムから観測値を生成する
def sys_observe(x):
    v = np.random.normal(0, Sigma_v)
    return x[0] + v

# システムの状態を更新する
def sys_update(x):
    a = np.random.normal(0, Sigma_a)
    return np.dot(F, x) + a * G

# x,p(k-1|k-1) から x,p(k|k-1) を予測する
def predict(x, p):
    return np.dot(F, x), np.dot(np.dot(F, p), F.T) + Sigma_a * np.outer(G, G)

# 予測値 x,p(k|k-1) と観測値 y から状態 x,p(k|k) を推定する
def update(x, p, y):
    e = y - x[0]
    s = Sigma_v + np.dot(np.dot(H, p), H)
    k = np.dot(p, H) / s
    return (x + e * k), (p - np.dot(np.outer(k, H), p))


# simulation
sys_x = np.array([0, 0])
x = np.array([0, 0])
p = np.array([[0, 0],
              [0, 0]])

for i in range(1000):
    # system
    sys_x = sys_update(sys_x)
    y = sys_observe(sys_x)

    # kalman filter
    x, p = predict(x, p)
    x, p = update(x, p, y)

    # y    : 観測位置
    # sys_x: 位置と速度の真値
    # x    : 位置と速度の推定値
    # p    : 推定誤差の共分散行列
    #        p[0,0] は位置推定値の分散、p[1,1]は速度推定値の分散
    print("{0} {1} {2} {3} {4} {5} {6} {7} {8}".format(
        y, sys_x[0], sys_x[1], x[0], x[1], p[0, 0], p[1, 1], p[0, 1], p[1, 0]))

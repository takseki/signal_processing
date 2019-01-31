import numpy as np

# Kalman filterによる位置推定
# 内部状態: (位置, 速度)
# 観測量 : 位置
# 等速運動であるが、速度がステップ的に変化, 推定側は変化タイミングを知らない

# constants
dt = 0.01
F = np.array([[1, dt],
              [0, 1]])
G = np.array([0, 1])
H = np.array([1, 0])
Sigma_a = 0.1    # ランダムに加わる速度, 推定側のみ
Sigma_v = 0.3    # 観測誤差

# システムから観測値を生成する
def sys_observe(x):
    v = np.random.normal(0, Sigma_v)
    return x[0] + v

# システムの状態を更新する
def sys_update(x):
    return np.dot(F, x)

# x,p(k-1|k-1) から x,p(k|k-1) を予測する
def predict(x, p):
    # モデル側は速度に白色雑音が乗るわけではないが、推定側はそれを仮定する
    # Sigma_a を入れないと追従できない
    return np.dot(F, x), np.dot(np.dot(F, p), F.T) + Sigma_a * np.outer(G, G)

# 予測値 x,p(k|k-1) と観測値 y から状態 x,p(k|k) を推定する
def update(x, p, y):
    e = y - x[0]
    s = Sigma_v + p[0, 0] #+ np.dot(np.dot(H, p), H)
    k = p[:, 0] / s # np.dot(p, H) / s
    # print("{0} {1}".format(k[0], k[1]))
    return (x + e * k), (p - np.dot(np.outer(k, H), p))

# simulation
sys_x = np.array([5, 1])
x = np.array([0, 0])
p = np.array([[0.1, 0],
              [0, 0.1]])

# IIRで良いんじゃね?
x_iir = 0
alpha = 0.1

for i in range(1000):
    # system
    sys_x = sys_update(sys_x)
    # 速度がステップ的に変化する
    if i == 200:
        sys_x[1] = -1
    elif i == 600:
        sys_x[1] = 0
    y = sys_observe(sys_x)

    # kalman filter
    x, p = predict(x, p)
    x, p = update(x, p, y)

    # IIR filter
    x_iir = (1 - alpha) * x_iir + alpha * y

    # y    : 観測位置
    # sys_x: 位置と速度の真値
    # x    : 位置と速度の推定値
    # p    : 推定誤差の共分散行列
    #        p[0,0] は位置推定値の分散、p[1,1]は速度推定値の分散
    print("{0} {1} {2} {3} {4} {5}".format(
        y, sys_x[0], sys_x[1], x[0], x[1], x_iir))

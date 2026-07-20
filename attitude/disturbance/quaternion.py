"""
四元数定义的函数
---------
normalize()
conjugate()
inverse()
multiply()
omega_matrix()
to_dcm()
from_axis_angle()
"""

import numpy as np
# 四元数的归一化
def normalize(q):

    return q / np.linalg.norm(q)


# 四元数共轭
def conjugate(q):
    q0, q1, q2, q3 = q
    return np.array([q0,-q1,-q2,-q3])



# 四元数求逆
def inverse(q):
    return conjugate(q) / np.dot(q, q)

# 四元数乘法
def multiply(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2

    return np.array([

        w1*w2 - x1*x2 - y1*y2 - z1*z2,

        w1*x2 + x1*w2 + y1*z2 - z1*y2,

        w1*y2 - x1*z2 + y1*w2 + z1*x2,

        w1*z2 + x1*y2 - y1*x2 + z1*w2

    ])

#omega矩阵
def omega_matrix(omega):

    wx, wy, wz = omega

    return np.array([

        [0,   -wx, -wy, -wz],

        [wx,   0,   wz, -wy],

        [wy,  -wz,  0,   wx],

        [wz,   wy, -wx,  0]

    ])

# 四元数运动学
def quaternion_dot(q, omega):

    Omega = omega_matrix(omega)
    return 0.5 * Omega @ q

# 四元数和方向余弦矩阵互转
def to_dcm(q):

    q = normalize(q)

    q0, q1, q2, q3 = q

    C = np.array([

        [  1-2*(q2*q2+q3*q3),

            2*(q1*q2-q0*q3),

            2*(q1*q3+q0*q2) ],

        [   2*(q1*q2+q0*q3),

            1-2*(q1*q1+q3*q3),

            2*(q2*q3-q0*q1)],

        [   2*(q1*q3-q0*q2),

            2*(q2*q3+q0*q1),

            1-2*(q1*q1+q2*q2)]

    ])
    return C

# 轴角转四元数矩阵
def from_axis_angle(axis, angle):

    axis = axis / np.linalg.norm(axis)

    q0 = np.cos(angle/2)

    qv = axis * np.sin(angle/2)

    return normalize(np.array([q0,qv[0],qv[1],qv[2]]))

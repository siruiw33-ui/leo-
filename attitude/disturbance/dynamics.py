"""
姿态动力学
"""

import numpy as np
from quaternion import (quaternion_dot,normalize)
from disturbance.disturbance import disturbance_torque
from constants import I


I_inv = np.linalg.inv(I)

#姿态动力学
def attitude_dynamics(t,state,r,v,wheel_speed):


    #提取四元数
    q = state[0:4]
    q = normalize(q)

    #角速度
    omega = state[4:7]

    #四元数运动学
    dq = quaternion_dot(q, omega)

    #干扰力矩
    Td = disturbance_torque(q,r,v,wheel_speed,t)

    #控制力矩
    Tc = np.zeros(3)

    #总力矩
    T = Tc + Td


    #欧拉动力学方程
    domega = I_inv @ (T -np.cross(omega,I @ omega))

    #合并状态倒数
    dx = np.concatenate((dq,domega))

    return dx
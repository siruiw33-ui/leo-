"""
计算重力梯度力矩
"""
import numpy as np
from constants import MU,I
from attitude.quaternion import to_dcm


def gravity_gradient(q,r):
    #计算模长
    r_norm = np.linalg.norm(r)

    if r_norm < 1e-8:
         return np.zeros(3)

    C = to_dcm(q)

    #惯性系下的地心位置向量投影到卫星的机体坐标系下
    r_body = C.T @ r
    #获得机体系下的单位方向向量
    e = r_body / r_norm

    #计算重力梯度力矩
    torque = (3.0 * MU / r_norm**3) * np.cross(e, I @ e)

    return torque

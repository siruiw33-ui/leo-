"""
太阳光压力矩
"""

import numpy as np
from orbit.SRP import SUN_DIRECTION
from constants import AREA, P_SRP, CR,CG, CP
from attitude.quaternion import to_dcm

def srp_torque(q,r,v):

    C = to_dcm(q)

    #用转置矩阵将惯性系下太阳方向投影到本体系
    s_body = C.T @ SUN_DIRECTION

    #归一化，确保太阳光方向为单位向量
    s_body = s_body / np.linalg.norm(s_body)

    #定义卫星迎风面单位法向量
    n = np.array([1.0,0.0,0.0])

    #太阳光和迎风面法线夹角
    cos_theta = np.dot(n,s_body)

    if cos_theta <= 0:
        return np.zeros(3)

    #计算太阳光压力
    F = (P_SRP * AREA * CR * cos_theta* s_body)

    #计算力臂
    arm = CP - CG

    #计算太阳光压力矩
    torque = np.cross(arm,F)
    return torque
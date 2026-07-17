"""
计算空气动力矩
"""
import numpy as np
from constants import CD,AREA,CG, CP
from attitude.quaternion import to_dcm
from orbit.drag import (relative_velocity,atmospheric_density)


# 空气动力矩定义
def aerodynamic_torque(q,r,v):
    rho = atmospheric_density(r)

    #相对速度
    v_rel = relative_velocity(r, v)
    speed = np.linalg.norm(v_rel)

    #速度过低，则力矩为0
    if speed < 1e-8:
        return np.zeros(3)

    #改变速度至身体坐标系
    C = to_dcm(q)
    v_body = C.T @ v_rel
    e_v = v_body / speed

    #空气动阻力公式计算
    F = ( -0.5* rho* speed**2* CD* AREA * e_v)

    #力臂
    arm = CP - CG

    #空气动力矩
    torque = np.cross(arm,F)
    return torque
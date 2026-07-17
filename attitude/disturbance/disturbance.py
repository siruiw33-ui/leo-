"""
总扰动力矩
"""

import numpy as np

from attitude.disturbance.gravity_gradient import gravity_gradient
from attitude.disturbance.aerodynamic import aerodynamic_torque
from attitude.disturbance.magnetic_torque import magnetic_torque
from attitude.disturbance.srp_torque import srp_torque
from attitude.disturbance.reaction_wheel import reaction_wheel_torque


def disturbance_torque(q,r,v,wheel_speed,t):

    # 重力梯度矩
    T_gg = gravity_gradient(q,r)

    # 空气动力矩
    T_drag = aerodynamic_torque(q,r,v)

    # 地磁扰动干扰力矩
    T_mag = magnetic_torque(t,q,r)

    # 太阳压力矩
    T_srp = srp_torque(q,r,v)

    # 反作用飞轮扰动力矩
    T_rw = reaction_wheel_torque(wheel_speed,t)

    # 总扰动矩
    Td = T_gg + T_drag + T_mag + T_srp + T_rw

    detail = {
        "gravity_gradient": T_gg,
        "aerodynamic": T_drag,
        "magnetic": T_mag,
        "solar_radiation": T_srp,
        "reaction_wheel": T_rw,
    }

    return Td, detail
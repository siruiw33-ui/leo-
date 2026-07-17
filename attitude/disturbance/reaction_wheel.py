"""
反向飞轮扰动力矩

1. 静不平衡力
2. 动不平衡力矩
3. 谐波扰动
4. Campbell 频率模型
"""

import numpy as np

# 飞轮数据
# 静不平衡 (kg*m)
MU_STATIC = 2.0e-6

# 动不平衡 (kg*m²)
MU_DYNAMIC = 5.0e-8

# 飞轮安装位置 (m)
RW_POSITION = np.array([0.20,0.15,0.10])

# 旋转轴
RW_AXIS = np.array([0.0,0.0,1.0])

# 谐波系数
A1 = 2.0e-6
A2 = 6.0e-7
A3 = 2.5e-7

"""
静不平衡力
"""
def static_imbalance_force(wheel_speed):
    F = MU_STATIC * wheel_speed ** 2 * RW_AXIS
    return F

"""
飞轮动不平衡力矩
"""
def dynamic_imbalance_torque(wheel_speed):

    M = MU_DYNAMIC * wheel_speed ** 2 * RW_AXIS
    return  M


"""
飞轮谐波扰动
"""
def harmonic_disturbance(wheel_speed,t):

    h = (A1*np.sin(wheel_speed*t)+
         A2*np.sin(2*wheel_speed*t)+
         A3*np.sin(3*wheel_speed*t))

    return h * RW_AXIS

"""
Campbell模型
"""
def campbell_modes(
        wheel_speed):

    return np.array([wheel_speed,
                     2*wheel_speed,
                     3*wheel_speed,
                     4*wheel_speed,
                     5*wheel_speed])


#总扰动力矩
def reaction_wheel_torque(wheel_speed,t):

    F_static = static_imbalance_force(wheel_speed)

    T_static = np.cross(RW_POSITION,F_static)
    T_dynamic = dynamic_imbalance_torque(wheel_speed)
    T_harmonic = harmonic_disturbance(wheel_speed,t)

    T_total = (T_static+ T_dynamic+ T_harmonic)

    return T_total
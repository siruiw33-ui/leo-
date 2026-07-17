''''
太阳光压力模型
'''

import numpy as np
from constants import AREA, P_SRP, CR,MASS


def SUN_DIRECTION(t):
    """
    计算ECI坐标系中的太阳方向（简化模型）
    参考：天文年历简化公式
    """
    # 从2000年1月1日12:00起算的天数
    # 这里简化：假设t是秒，转换为天数
    days = t / 86400.0

    # 太阳黄经 (度): 约 280.46° + 0.985647° × 天数
    ecliptic_longitude = np.radians(280.46 + 0.985647 * days)

    # 黄道倾角 (约23.44°)
    obliquity = np.radians(23.44)

    # 太阳在ECI中的方向
    s_x = np.cos(ecliptic_longitude)
    s_y = np.cos(obliquity) * np.sin(ecliptic_longitude)
    s_z = np.sin(obliquity) * np.sin(ecliptic_longitude)

    s = np.array([s_x, s_y, s_z])
    return s / np.linalg.norm(s)


def srp_acceleration(r,t):

    coefficient = (P_SRP * CR * AREA/ MASS)
    a_srp = coefficient * SUN_DIRECTION(t)

    return a_srp

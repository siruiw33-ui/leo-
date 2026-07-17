"""
大气阻力模型
"""

import numpy as np
from constants import RE, CD, AREA, OMEGA_E, H0,RHO0,HS,MASS


def atmospheric_density(r):
    altitude = np.linalg.norm(r) - RE
    rho = RHO0 * np.exp(-(altitude - H0) / HS)
    return rho

def relative_velocity(r, v):

    omega = np.array([0.0, 0.0, OMEGA_E])
    v_atm = np.cross(omega, r)

    return v - v_atm

def drag_acceleration(r, v):
    rho = atmospheric_density(r)
    v_rel = relative_velocity(r, v)
    speed = np.linalg.norm(v_rel)
    if speed < 1e-8:
        return np.zeros(3)
    coefficient = (-0.5 * rho* CD* AREA/ MASS )

    a_drag = coefficient * speed * v_rel

    return a_drag
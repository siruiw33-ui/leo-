"""
地磁模型
"""
import numpy as np
def magnetic_field(t):
    B0=3e-5
    Torbit=5400

    theta=2*np.pi*t/Torbit

    B = np.array([B0*np.cos(theta),B0*np.sin(theta),0.5*B0])

    return B
"""
太阳敏感器
z = s_body + noise
"""

import numpy as np

class SunSensor:

    def __init__(
        self,
        noise_std = 1e-3,
        bias = None,
        dt = 1.0 ):

        if bias is None:
            bias = np.zeros(3)
        self.bias = np.array(bias,dtype=float)

        #噪声标准差
        self.noise_std = noise_std

        #采样时间
        self.dt = dt

    #测量模拟
    def measure(self,sun_vector_body):

        noise = (np.random.randn(3) * self.noise_std)

        sun_measure = (sun_vector_body + self.bias + noise)
        sun_measure = (sun_measure / np.linalg.norm(sun_measure))

        return sun_measure
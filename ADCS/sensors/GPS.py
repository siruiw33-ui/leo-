"""
GPS
position_m = position + noise
velocity_m = velocity + noise
"""

import numpy as np

class GPS:

    def __init__(
        self,
        position_bias = None,
        velocity_bias = None,
        position_noise_std = 5.0,
        velocity_noise_std = 0.05,
        dt = 1.0):

        if position_bias is None:
            position_bias = np.zeros(3)
        self.position_bias = np.array(position_bias,dtype = float)

        if velocity_bias is None:
            velocity_bias = np.zeros(3)
        self.velocity_bias = np.array(velocity_bias,dtype = float )

        #位置测量白噪声标准差
        self.position_noise_std = position_noise_std

        #速度测量白噪声标准差
        self.velocity_noise_std = velocity_noise_std

        #采样周期
        self.dt = dt


    #模拟测量
    def measure(self, position_true,velocity_true):
        # 位置噪声
        position_noise = ( np.random.randn(3) * self.position_noise_std)

        # 速度噪声
        velocity_noise = ( np.random.randn(3) * self.velocity_noise_std)

        position_measure = (position_true + self.position_bias + position_noise)

        velocity_measure = (velocity_true + self.velocity_bias + velocity_noise)

        return position_measure,velocity_measure
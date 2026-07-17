"""
陀螺仪
omega_m = omega + bias + noise
"""
import numpy as np

class Gyroscope:

    def __init__(
        self,
        bias = None,
        noise_std = 1e-5,
        bias_random_walk = 1e-7,
        dt = 0.01 ):

        # 初始零偏
        if bias is None:
            bias = np.zeros(3)
        self.bias=np.array(bias,dtype=float)

        # 白噪声
        self.noise_std = noise_std

        # 零偏漂移系数
        self.bias_random_walk = bias_random_walk

        # 采样周期
        self.dt = dt


    def update_bias(self):
        wb=(np.random.randn(3) * self.bias_random_walk)
        self.bias += (wb * np.sqrt(self.dt))


    def measure(self,omega):
        #更新偏置
        self.update_bias()

        #计算噪声
        noise = (np.random.randn(3) * self.noise_std)

        #最终角速度
        omega_measure = (omega + self.bias +noise)

        return omega_measure

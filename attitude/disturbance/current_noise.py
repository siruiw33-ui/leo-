"""
磁力矩器电流噪声模型
"""

import numpy as np

class MagnetorquerCurrentNoise:

    def __init__(
        self,
        tau=0.01,
        lambda_bias=0.001,
        sigma_current=1e-4,
        sigma_bias=1e-6,
        current_limit=0.5,):

        self.tau = tau
        self.lambda_bias = lambda_bias

        self.sigma_current = sigma_current
        self.sigma_bias = sigma_bias

        self.current_limit = current_limit

        self.current = np.zeros(3)
        self.bias = np.zeros(3)

    def reset(self):
        self.current[:] = 0.0
        self.bias[:] = 0.0

    def saturation(self, current):
        return np.clip(current, -self.current_limit, self.current_limit)

    def step(self, current_cmd, dt):

        current_cmd = np.asarray(current_cmd)
        # 白噪音
        current_noise = (self.sigma_current* np.random.randn(3))

        # 电流偏置
        bias_noise = (self.sigma_bias * np.random.randn(3))
        self.bias += (-self.lambda_bias* self.bias+ bias_noise* np.sqrt(dt))

        # 磁力矩器电流动态模型
        current_dot = (-self.current + current_cmd + self.bias + current_noise) / self.tau
        self.current += current_dot * dt

        current_actual = self.saturation( self.current)

        return current_actual
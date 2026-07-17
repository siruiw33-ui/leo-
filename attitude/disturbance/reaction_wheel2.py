"""
飞轮扰动模型
"""

import numpy as np

class ReactionWheelImbalance:

    def __init__(
        self,
        mass,
        eccentricity,
        inertia_transverse,
        mounting_position,
        imbalance_angle=0.0,
        phase_force=0.0,
        phase_torque=0.0,
        force_harmonics=None,
        torque_harmonics=None,):

        # 飞轮质量
        self.mass = mass

        # 质心偏心距
        self.eccentricity = eccentricity

        # 横向转动惯量
        self.inertia_transverse = (inertia_transverse)

        # 飞轮安装位置
        self.mounting_position = np.asarray(mounting_position,dtype=float)

        # 惯量主轴与旋转轴之间的夹角
        self.imbalance_angle = (imbalance_angle)

        # 静不平衡力相位
        self.phase_force = phase_force

        # 动不平衡力偶相位
        self.phase_torque = phase_torque

        # 飞轮旋转角度
        self.theta = 0.0

        #高阶谐波力
        self.force_harmonics = (force_harmonics
            if force_harmonics is not None
            else {} )

        #高阶谐波力矩
        self.torque_harmonics = ( torque_harmonics
            if torque_harmonics is not None
            else {} )

    #重置角度
    def reset(self):
        self.theta = 0.0

    #积分，更新飞轮转角
    def update_angle(self,omega,dt):
        self.theta += omega * dt

    # 静不平衡振动力
    def static_imbalance_force(self,omega ):
        # 当前力的相位
        theta = (self.theta + self.phase_force)

        # 偏心距
        e = self.eccentricity

        # 不平衡力幅值
        force_amplitude = (self.mass * e * omega**2)

        # 周期性不平衡力
        force = (force_amplitude * np.array([np.cos(theta), np.sin(theta),0.0,]))

        return force


    # 动不平衡扰动力偶
    def dynamic_imbalance_torque(self,omega ):

        # 当前力偶的相位
        theta = (self.theta + self.phase_torque)

        # 动不平衡角
        alpha = (self.imbalance_angle)

        # 力偶幅值
        torque_amplitude = (self.inertia_transverse * alpha * omega**2)

        # 周期性扰动力偶
        torque = ( torque_amplitude * np.array([np.cos(theta),np.sin(theta),0.0, ]))

        return torque

    #高阶谐波力
    def harmonic_force(self, omega):
        force = np.zeros(3)

        for n, parameter in (self.force_harmonics.items()):

            #谐波系数
            coefficient = (parameter["coefficient"])

            phase = (parameter.get("phase", 0.0))

            amplitude = (coefficient * omega ** 2)

            angle = (n * self.theta + phase )

            force += amplitude * np.array([np.cos(angle),np.sin(angle),0.0,])

        return force

    #高阶谐波力矩
    def harmonic_torque(self,omega):

        torque = np.zeros(3)

        for n, parameter in (self.torque_harmonics.items()):
            coefficient = (parameter["coefficient"])

            phase = (parameter.get("phase",0.0))

            amplitude = (coefficient * omega ** 2)

            angle = (n * self.theta + phase)

            torque += amplitude * np.array([np.cos(angle),np.sin(angle),0.0,])

        return torque

    # 静不平衡力引起的安装力矩
    def static_imbalance_torque(self,force):
        torque = np.cross(self.mounting_position, force)
        return torque


    # 总扰动力矩
    def total_disturbance(self,omega,dt):

        # 更新飞轮旋转角度
        self.update_angle(omega,dt)

        # 静不平衡振动力
        force_1x = (self.static_imbalance_force(omega))

        force_higher = (self.harmonic_force(omega))

        force_total = (force_higher + force_1x)
        # 静不平衡力产生的力矩
        static_torque = (self.static_imbalance_torque(force_total))

        # 动不平衡直接产生的力偶
        dynamic_torque = (self.dynamic_imbalance_torque(omega))

        harmonic_torque = (self.harmonic_torque(omega))
        # 总扰动力矩
        total_torque = (static_torque + dynamic_torque + harmonic_torque)

        return {
            "force_1x": force_1x,
            "force_higher": force_higher,
            "force_total": force_total,
            "static_torque": static_torque,
            "dynamic_torque": dynamic_torque,
            "harmonic_torque": harmonic_torque,
            "total_torque": total_torque,
        }